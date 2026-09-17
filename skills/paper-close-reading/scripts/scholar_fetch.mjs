#!/usr/bin/env node
// Node-native transport only. Parsing and normalization stay in the Python
// launcher so Node and curl cannot disagree about entities, links, or counts.
import fs from 'node:fs/promises';

function nowIso() { return new Date().toISOString(); }
function option(name, fallback = null) { const args = process.argv.slice(2); const i = args.indexOf(name); return i >= 0 ? args[i + 1] : fallback; }
function emit(value, code = 0) { console.log(JSON.stringify(value)); process.exitCode = code; }

const url = option('--url');
const timeoutMs = Number(option('--timeout-ms', '20000'));
const fixture = option('--input-file');
const fixtureContentType = option('--input-content-type', '');
const maxBytes = 8 * 1024 * 1024;
const started = nowIso();
const begin = performance.now();
try {
  let body;
  let status = 200;
  let contentType = fixtureContentType || 'fixture';
  if (fixture) {
    if ((await fs.stat(fixture)).size > maxBytes) throw Object.assign(new Error('Fixture exceeds 8 MiB'), { kind: 'response_too_large' });
    body = await fs.readFile(fixture);
  } else {
    const response = await fetch(url, { method: 'GET', credentials: 'include', signal: AbortSignal.timeout(timeoutMs) });
    status = response.status;
    contentType = response.headers.get('content-type') ?? '';
    if ([401, 403, 407, 429, 503].includes(status) || status !== 200) {
      await response.body?.cancel();
      body = new Uint8Array();
    } else {
      const chunks = [];
      let total = 0;
      for await (const chunk of response.body) {
        total += chunk.byteLength;
        if (total > maxBytes) throw Object.assign(new Error('Response exceeds 8 MiB'), { kind: 'response_too_large' });
        chunks.push(chunk);
      }
      body = Buffer.concat(chunks, total);
    }
  }
  if (body.byteLength > maxBytes) {
    emit({ status: 'response_too_large', transport: 'node-fetch', fetched_at: started, elapsed_ms: Math.round(performance.now() - begin), requested_url: url, http_status: status, content_type: contentType, error: `Response exceeds ${maxBytes} bytes` }, 1);
  } else if ([401, 403, 407, 429, 503].includes(status)) {
    emit({ status: 'access_restricted', transport: 'node-fetch', fetched_at: started, elapsed_ms: Math.round(performance.now() - begin), requested_url: url, http_status: status, content_type: contentType, error: `Scholar returned HTTP ${status}; no transport retry` }, 1);
  } else if (status !== 200) {
    emit({ status: 'http_error', transport: 'node-fetch', fetched_at: started, elapsed_ms: Math.round(performance.now() - begin), requested_url: url, http_status: status, content_type: contentType, error: `Scholar returned HTTP ${status}` }, 1);
  } else {
    emit({ status: 'raw_ok', transport: 'node-fetch', fetched_at: started, elapsed_ms: Math.round(performance.now() - begin), requested_url: url, http_status: status, content_type: contentType, body_base64: Buffer.from(body).toString('base64') });
  }
} catch (error) {
  const kind = error.kind ?? (['TimeoutError', 'AbortError'].includes(error.name) ? 'timeout' : 'transport_error');
  emit({ status: kind, transport: 'node-fetch', fetched_at: started, elapsed_ms: Math.round(performance.now() - begin), requested_url: url, http_status: null, error: error.message }, 1);
}
