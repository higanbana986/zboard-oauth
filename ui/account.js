(() => {
  const $ = (id) => document.getElementById(id);
  let providers = [], bindings = [], busy = false;
  const resize = oauthBridge.observeSize(document.querySelector('main'));
  const providerName = (id) => providers.find((item) => item.id === id)?.name || id;
  const setNotice = (text, error = false) => { $('notice').textContent = text; $('notice').className = error ? 'error' : 'success'; resize(); };
  const setBusy = (value) => { busy = value; for (const button of document.querySelectorAll('button')) button.disabled = value || button.textContent === '已绑定'; };
  function details(binding) {
    const box = document.createElement('div'); box.className = 'identity-details';
    const title = document.createElement('strong'); title.textContent = providerName(binding.provider_id); box.append(title);
    for (const [label, value] of [['Issuer', binding.issuer], ['第三方账号标识', binding.subject], ['绑定时间', new Date(binding.created_at).toLocaleString()]]) {
      const line = document.createElement('small'); line.textContent = `${label}：${value || '—'}`; box.append(line);
    }
    return box;
  }
  function render() {
    $('bindings').replaceChildren(); $('providers').replaceChildren(); $('empty-bindings').hidden = bindings.length > 0; $('empty-providers').hidden = providers.length > 0;
    for (const binding of bindings) {
      const row = document.createElement('article'); row.append(details(binding));
      const button = document.createElement('button'); button.type = 'button'; button.textContent = '解绑';
      button.addEventListener('click', () => unlink(binding.id)); row.append(button); $('bindings').append(row);
    }
    for (const provider of providers) {
      const row = document.createElement('article'); const name = document.createElement('strong'); name.textContent = provider.name; row.append(name);
      const linked = bindings.some((binding) => binding.provider_id === provider.id);
      const button = document.createElement('button'); button.type = 'button'; button.textContent = linked ? '已绑定' : '绑定账号'; button.disabled = linked;
      if (!linked) button.addEventListener('click', () => bind(provider.id)); row.append(button); $('providers').append(row);
    }
    resize();
  }
  async function refresh() {
    [providers, bindings] = await Promise.all([oauthBridge.request('identity.providers.list'), oauthBridge.request('identity.bindings.list')]); render();
  }
  async function bind(providerID) {
    if (busy) return; setBusy(true); setNotice('正在验证账户并处理请求…');
    try { await oauthBridge.request('identity.bind.start', { provider_id: providerID }); }
    catch (error) { setNotice(error.message || '绑定未开始，请检查提供方状态。', true); setBusy(false); }
  }
  async function unlink(identityID) {
    if (busy) return; setBusy(true); setNotice('正在验证账户并处理请求…');
    try { await oauthBridge.request('identity.binding.unlink', { identity_id: identityID }); await refresh(); setNotice('第三方账号已解绑。'); }
    catch (error) { setNotice(error.message || '解绑失败，请刷新重试。', true); }
    finally { setBusy(false); }
  }
  (async () => { try { const context = await oauthBridge.request('context.load'); if (context.plugin_id !== 'zboard.oauth' || context.slot !== 'account.security.identities' || context.surface !== 'account') throw new Error('invalid slot'); await refresh(); } catch { setNotice('OAuth 关联账号加载失败。', true); } })();
})();
