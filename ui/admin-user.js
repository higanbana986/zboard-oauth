(() => {
  const bindings = document.getElementById('bindings'); const empty = document.getElementById('empty'); const notice = document.getElementById('notice');
  let providers = [];
  const resize = oauthBridge.observeSize(document.querySelector('main'));
  function row(binding) {
    const item = document.createElement('article'); const details = document.createElement('div'); details.className = 'identity-details';
    const title = document.createElement('strong'); title.textContent = providers.find((provider) => provider.id === binding.provider_id)?.name || binding.provider_id; details.append(title);
    for (const [label, value] of [['插件发布者', binding.publisher], ['Issuer', binding.issuer], ['第三方账号标识', binding.subject], ['绑定时间', new Date(binding.created_at).toLocaleString()]]) { const line = document.createElement('small'); line.textContent = `${label}：${value || '—'}`; details.append(line); }
    const button = document.createElement('button'); button.type = 'button'; button.textContent = '解除绑定'; button.addEventListener('click', async () => { button.disabled = true; notice.textContent = '正在解除绑定…'; try { await oauthBridge.request('identity.binding.unlink', { identity_id: binding.id }); await load(); notice.textContent = '绑定已解除。'; notice.className = 'success'; } catch { notice.textContent = '解除绑定失败，请刷新后重试。'; notice.className = 'error'; button.disabled = false; } });
    item.append(details, button); return item;
  }
  async function load() { const values = await oauthBridge.request('identity.bindings.list'); if (!Array.isArray(values)) throw new Error('invalid bindings'); bindings.replaceChildren(...values.map(row)); empty.hidden = values.length > 0; resize(); }
  (async () => { try { const context = await oauthBridge.request('context.load'); if (context.plugin_id !== 'zboard.oauth' || context.slot !== 'admin.user.identities' || context.surface !== 'admin' || !context.target_user_id) throw new Error('invalid slot'); providers = await oauthBridge.request('identity.providers.list'); if (!Array.isArray(providers)) throw new Error('invalid providers'); await load(); } catch { notice.textContent = 'OAuth 关联账号加载失败。'; notice.className = 'error'; resize(); } })();
})();
