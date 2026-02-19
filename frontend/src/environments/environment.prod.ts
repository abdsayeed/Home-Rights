export const environment = {
  production: true,
  apiUrl: '/api',
  wsUrl: window.location.protocol === 'https:' ? 'wss://' + window.location.host : 'ws://' + window.location.host
};
