const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function fixture(page, responses) {
  const html = fs.readFileSync(path.join(__dirname, `../ui/${page}.html`), 'utf8');
  const ids = [...html.matchAll(/id="([^"]+)"/g)].map((match) => match[1]);
  const elements = new Map();
  const created = [];
  const element = (tag = 'div') => ({
    tag, textContent: '', className: '', type: '', value: '', disabled: false, hidden: false, children: [], listeners: {},
    addEventListener(name, fn) { this.listeners[name] = fn; },
    append(...values) { this.children.push(...values); },
    replaceChildren(...values) { this.children = values; },
    querySelectorAll(selector) { return selector === 'button' ? this.children.filter((child) => child.tag === 'button') : []; },
  });
  for (const id of ids) elements.set(id, element());
  const calls = [];
  const document = {
    querySelector: () => ({}),
    getElementById: (id) => elements.get(id),
    createElement: (tag) => { const value = element(tag); created.push(value); return value; },
    querySelectorAll: (selector) => selector === 'button' ? created.filter((value) => value.tag === 'button') : [],
    documentElement: { scrollHeight: 200 },
  };
  const oauthBridge = { observeSize: () => () => {}, resize() {}, async request(type, body) { calls.push({ type, body }); const value = responses[type]; return typeof value === 'function' ? value(body) : value; } };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, `../ui/${page}.js`), 'utf8'), { document, oauthBridge, Date, Array, Error });
  return { elements, calls };
}

test('login slot renders only its providers and starts through the identity bridge', async () => {
  const f = fixture('login', {
    'context.load': { plugin_id: 'zboard.oauth', surface: 'public', slot: 'auth.login.methods' },
    'identity.providers.list': [{ id: 'zboard.oauth~github', name: 'GitHub' }],
    'identity.login.start': {},
  });
  await new Promise((resolve) => setImmediate(resolve));
  const button = f.elements.get('providers').children[0];
  assert.equal(button.textContent, '使用 GitHub 登录');
  await button.listeners.click();
  assert.deepEqual(JSON.parse(JSON.stringify(f.calls.at(-1))), { type: 'identity.login.start', body: { provider_id: 'zboard.oauth~github' } });
});

test('account slot shows identity details without publisher attribution and delegates password confirmation to the host', async () => {
  const f = fixture('account', {
    'context.load': { plugin_id: 'zboard.oauth', surface: 'account', slot: 'account.security.identities' },
    'identity.providers.list': [{ id: 'zboard.oauth~github', name: 'GitHub' }],
    'identity.bindings.list': [{ id: 'binding', provider_id: 'zboard.oauth~github', publisher: 'official', issuer: 'https://github.com', subject: '123', created_at: '2026-09-10T00:00:00Z' }],
    'identity.binding.unlink': {},
  });
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(f.elements.get('bindings').children.length, 1);
  assert.match(f.elements.get('bindings').children[0].children[0].children[1].textContent, /github.com/);
  assert.ok(f.elements.get('bindings').children[0].children[0].children.every((item) => !item.textContent.includes('official')));
  await f.elements.get('bindings').children[0].children[1].listeners.click();
  assert.deepEqual(JSON.parse(JSON.stringify(f.calls.find((call) => call.type === 'identity.binding.unlink').body)), { identity_id: 'binding' });
});

test('admin user slot requires a target and unlinks through the scoped bridge', async () => {
  const f = fixture('admin-user', {
    'context.load': { plugin_id: 'zboard.oauth', surface: 'admin', slot: 'admin.user.identities', target_user_id: 9 },
    'identity.providers.list': [{ id: 'zboard.oauth~google', name: 'Google' }],
    'identity.bindings.list': [{ id: 'binding', provider_id: 'zboard.oauth~google', publisher: 'official', issuer: 'https://accounts.google.com', subject: 'abc', created_at: '2026-09-10T00:00:00Z' }],
    'identity.binding.unlink': {},
  });
  await new Promise((resolve) => setImmediate(resolve));
  assert.equal(f.elements.get('bindings').children[0].children[0].children[0].textContent, 'Google');
  await f.elements.get('bindings').children[0].children[1].listeners.click();
  assert.deepEqual(JSON.parse(JSON.stringify(f.calls.find((call) => call.type === 'identity.binding.unlink').body)), { identity_id: 'binding' });
});
