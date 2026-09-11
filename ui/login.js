(() => {
  const content = document.getElementById('content');
  const providers = document.getElementById('providers');
  const notice = document.getElementById('notice');
  const resize = oauthBridge.observeSize(document.querySelector('main'));
  const fail = (message) => { notice.textContent = message; notice.className = 'error'; resize(); };
  async function start(provider) {
    for (const button of providers.querySelectorAll('button')) button.disabled = true;
    notice.textContent = '正在前往授权服务…';
    try { await oauthBridge.request('identity.login.start', { provider_id: provider.id }); }
    catch { fail('第三方登录暂不可用，请重试或使用邮箱登录。'); for (const button of providers.querySelectorAll('button')) button.disabled = false; }
  }
  async function load() {
    try {
      const context = await oauthBridge.request('context.load');
      if (context.plugin_id !== 'zboard.oauth' || context.slot !== 'auth.login.methods' || context.surface !== 'public') throw new Error('invalid slot');
      const values = await oauthBridge.request('identity.providers.list');
      if (!Array.isArray(values)) throw new Error('invalid providers');
      providers.replaceChildren();
      for (const provider of values) {
        const button = document.createElement('button');
        button.type = 'button'; button.textContent = `使用 ${provider.name} 登录`;
        button.addEventListener('click', () => start(provider)); providers.append(button);
      }
      content.hidden = values.length === 0; notice.textContent = ''; resize();
    } catch { fail('第三方登录入口加载失败。'); }
  }
  load(); resize();
})();
