declare var require: any;
export const environment = {
  production: true,
  name: require('../../package.json').name,
  applicationId: require('../../package.json').id,
  version: require('../../package.json').version,
  versionCode: require('../../package.json').versionCode,
  proxyApiUrl: 'https://medix.xlayer.in',
  // proxyApiUrl: 'ohzas.xlayer.in',
  proxySocketUrl: 'wss://medix.xlayer.in',
  firebase: {},
  google: {
    // TODO CHANGE APIKEY
    // apiKey: 'AIzaSyDcT9_4s5jIwcS7yAsO-JexPEBDgbMZ3tY'
    apiKey: 'AIzaSyBdHjvhOdmS2Et0vfU2PkuZnkuVkRUPcUE'
  },
  xOrigin: {
    key: 'gAAAAABeka_J124HZJ0ERgFU_K7L3HeMFCUMaqRXuPd0SaaBzO09BdndXhZPROmE2DKwMq' +
    'vWbGEiAtbIe1BVRAC_olGghhy9rM8j6ztXt5xOpwuI_SjMywQ=',
  },
  xApi: {
    key: 'gAAAAABeka_JckndPuP1ge5NpszUtBMERYjmqlh7aWZ7VZmJxIbu3f0eLUfv6KKEx45CkIT' +
    'yLNQJ_EWAntLPeWgEGJ6OLvF_bLmpWxBRIn3YAiDeIKEwxKs=',
  }
};

export const palete = {
    primary: '#D32F2F',
    accent: '#E65100',
    warm: '#C2185B',
    name: '#D50000',
    secondary: '#D81B60',
    tertiary: '#8E24AA',
    quaternary: '#5E35B1',
    quinary: '#3949AB',
    secondaryLight: '#E91E63',
    tertiaryLight: '#9C27B0',
    quaternaryLight: '#673AB7',
    quinaryLight: '#3F51B5'
};

