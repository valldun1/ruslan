const { contextBridge, ipcRenderer, webUtils } = require('electron')

contextBridge.exposeInMainWorld('hermesDesktop', {
  getConnection: profile => ipcRenderer.invoke('ruslan:connection', profile),
  revalidateConnection: () => ipcRenderer.invoke('ruslan:connection:revalidate'),
  touchBackend: profile => ipcRenderer.invoke('ruslan:backend:touch', profile),
  getGatewayWsUrl: profile => ipcRenderer.invoke('ruslan:gateway:ws-url', profile),
  openSessionWindow: (sessionId, opts) => ipcRenderer.invoke('ruslan:window:openSession', sessionId, opts),
  openNewSessionWindow: () => ipcRenderer.invoke('ruslan:window:openNewSession'),
  getBootProgress: () => ipcRenderer.invoke('ruslan:boot-progress:get'),
  getConnectionConfig: profile => ipcRenderer.invoke('ruslan:connection-config:get', profile),
  saveConnectionConfig: payload => ipcRenderer.invoke('ruslan:connection-config:save', payload),
  applyConnectionConfig: payload => ipcRenderer.invoke('ruslan:connection-config:apply', payload),
  testConnectionConfig: payload => ipcRenderer.invoke('ruslan:connection-config:test', payload),
  probeConnectionConfig: remoteUrl => ipcRenderer.invoke('ruslan:connection-config:probe', remoteUrl),
  oauthLoginConnectionConfig: remoteUrl => ipcRenderer.invoke('ruslan:connection-config:oauth-login', remoteUrl),
  oauthLogoutConnectionConfig: remoteUrl => ipcRenderer.invoke('ruslan:connection-config:oauth-logout', remoteUrl),
  profile: {
    get: () => ipcRenderer.invoke('ruslan:profile:get'),
    set: name => ipcRenderer.invoke('ruslan:profile:set', name)
  },
  api: request => ipcRenderer.invoke('ruslan:api', request),
  notify: payload => ipcRenderer.invoke('ruslan:notify', payload),
  requestMicrophoneAccess: () => ipcRenderer.invoke('ruslan:requestMicrophoneAccess'),
  readFileDataUrl: filePath => ipcRenderer.invoke('ruslan:readFileDataUrl', filePath),
  readFileText: filePath => ipcRenderer.invoke('ruslan:readFileText', filePath),
  selectPaths: options => ipcRenderer.invoke('ruslan:selectPaths', options),
  writeClipboard: text => ipcRenderer.invoke('ruslan:writeClipboard', text),
  saveImageFromUrl: url => ipcRenderer.invoke('ruslan:saveImageFromUrl', url),
  saveImageBuffer: (data, ext) => ipcRenderer.invoke('ruslan:saveImageBuffer', { data, ext }),
  saveClipboardImage: () => ipcRenderer.invoke('ruslan:saveClipboardImage'),
  getPathForFile: file => {
    try {
      return webUtils.getPathForFile(file) || ''
    } catch {
      return ''
    }
  },
  normalizePreviewTarget: (target, baseDir) => ipcRenderer.invoke('ruslan:normalizePreviewTarget', target, baseDir),
  watchPreviewFile: url => ipcRenderer.invoke('ruslan:watchPreviewFile', url),
  stopPreviewFileWatch: id => ipcRenderer.invoke('ruslan:stopPreviewFileWatch', id),
  setTitleBarTheme: payload => ipcRenderer.send('ruslan:titlebar-theme', payload),
  setNativeTheme: mode => ipcRenderer.send('ruslan:native-theme', mode),
  setTranslucency: payload => ipcRenderer.send('ruslan:translucency', payload),
  setPreviewShortcutActive: active => ipcRenderer.send('ruslan:previewShortcutActive', Boolean(active)),
  openExternal: url => ipcRenderer.invoke('ruslan:openExternal', url),
  fetchLinkTitle: url => ipcRenderer.invoke('ruslan:fetchLinkTitle', url),
  sanitizeWorkspaceCwd: cwd => ipcRenderer.invoke('ruslan:workspace:sanitize', cwd),
  settings: {
    getDefaultProjectDir: () => ipcRenderer.invoke('ruslan:setting:defaultProjectDir:get'),
    setDefaultProjectDir: dir => ipcRenderer.invoke('ruslan:setting:defaultProjectDir:set', dir),
    pickDefaultProjectDir: () => ipcRenderer.invoke('ruslan:setting:defaultProjectDir:pick')
  },
  revealLogs: () => ipcRenderer.invoke('ruslan:logs:reveal'),
  getRecentLogs: () => ipcRenderer.invoke('ruslan:logs:recent'),
  readDir: dirPath => ipcRenderer.invoke('ruslan:fs:readDir', dirPath),
  gitRoot: startPath => ipcRenderer.invoke('ruslan:fs:gitRoot', startPath),
  worktrees: cwds => ipcRenderer.invoke('ruslan:fs:worktrees', cwds),
  terminal: {
    dispose: id => ipcRenderer.invoke('ruslan:terminal:dispose', id),
    resize: (id, size) => ipcRenderer.invoke('ruslan:terminal:resize', id, size),
    start: options => ipcRenderer.invoke('ruslan:terminal:start', options),
    write: (id, data) => ipcRenderer.invoke('ruslan:terminal:write', id, data),
    onData: (id, callback) => {
      const channel = `ruslan:terminal:${id}:data`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)
      return () => ipcRenderer.removeListener(channel, listener)
    },
    onExit: (id, callback) => {
      const channel = `ruslan:terminal:${id}:exit`
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on(channel, listener)
      return () => ipcRenderer.removeListener(channel, listener)
    }
  },
  onClosePreviewRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('ruslan:close-preview-requested', listener)
    return () => ipcRenderer.removeListener('ruslan:close-preview-requested', listener)
  },
  onOpenUpdatesRequested: callback => {
    const listener = () => callback()
    ipcRenderer.on('ruslan:open-updates', listener)
    return () => ipcRenderer.removeListener('ruslan:open-updates', listener)
  },
  onDeepLink: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('ruslan:deep-link', listener)
    return () => ipcRenderer.removeListener('ruslan:deep-link', listener)
  },
  signalDeepLinkReady: () => ipcRenderer.invoke('ruslan:deep-link-ready'),
  onWindowStateChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('ruslan:window-state-changed', listener)
    return () => ipcRenderer.removeListener('ruslan:window-state-changed', listener)
  },
  onFocusSession: callback => {
    const listener = (_event, sessionId) => callback(sessionId)
    ipcRenderer.on('ruslan:focus-session', listener)
    return () => ipcRenderer.removeListener('ruslan:focus-session', listener)
  },
  onNotificationAction: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('ruslan:notification-action', listener)
    return () => ipcRenderer.removeListener('ruslan:notification-action', listener)
  },
  onPreviewFileChanged: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('ruslan:preview-file-changed', listener)
    return () => ipcRenderer.removeListener('ruslan:preview-file-changed', listener)
  },
  onBackendExit: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('ruslan:backend-exit', listener)
    return () => ipcRenderer.removeListener('ruslan:backend-exit', listener)
  },
  onPowerResume: callback => {
    const listener = () => callback()
    ipcRenderer.on('ruslan:power-resume', listener)
    return () => ipcRenderer.removeListener('ruslan:power-resume', listener)
  },
  onBootProgress: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('ruslan:boot-progress', listener)
    return () => ipcRenderer.removeListener('ruslan:boot-progress', listener)
  },
  // First-launch bootstrap progress -- emitted by the install.ps1 stage
  // runner in main.cjs (apps/desktop/electron/bootstrap-runner.cjs).
  // Renderer's install overlay subscribes to live events and queries the
  // current snapshot via getBootstrapState() to recover after a devtools
  // reload mid-bootstrap.
  getBootstrapState: () => ipcRenderer.invoke('ruslan:bootstrap:get'),
  resetBootstrap: () => ipcRenderer.invoke('ruslan:bootstrap:reset'),
  repairBootstrap: () => ipcRenderer.invoke('ruslan:bootstrap:repair'),
  cancelBootstrap: () => ipcRenderer.invoke('ruslan:bootstrap:cancel'),
  onBootstrapEvent: callback => {
    const listener = (_event, payload) => callback(payload)
    ipcRenderer.on('ruslan:bootstrap:event', listener)
    return () => ipcRenderer.removeListener('ruslan:bootstrap:event', listener)
  },
  getVersion: () => ipcRenderer.invoke('ruslan:version'),
  getRemoteDisplayReason: () => ipcRenderer.invoke('ruslan:get-remote-display-reason'),
  uninstall: {
    summary: () => ipcRenderer.invoke('ruslan:uninstall:summary'),
    run: mode => ipcRenderer.invoke('ruslan:uninstall:run', { mode })
  },
  updates: {
    check: () => ipcRenderer.invoke('ruslan:updates:check'),
    apply: opts => ipcRenderer.invoke('ruslan:updates:apply', opts),
    getBranch: () => ipcRenderer.invoke('ruslan:updates:branch:get'),
    setBranch: name => ipcRenderer.invoke('ruslan:updates:branch:set', name),
    onProgress: callback => {
      const listener = (_event, payload) => callback(payload)
      ipcRenderer.on('ruslan:updates:progress', listener)
      return () => ipcRenderer.removeListener('ruslan:updates:progress', listener)
    }
  },
  themes: {
    fetchMarketplace: id => ipcRenderer.invoke('ruslan:vscode-theme:fetch', id),
    searchMarketplace: query => ipcRenderer.invoke('ruslan:vscode-theme:search', query)
  }
})
