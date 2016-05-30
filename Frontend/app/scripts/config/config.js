var config = config || {};

config.development = {
  //api_url: '//127.0.0.1:8000/api'
  api_url: 'http://ec2-54-65-53-178.ap-northeast-1.compute.amazonaws.com/api'
};
config.staging = {
  api_url: '//ec2-54-65-53-178.ap-northeast-1.compute.amazonaws.com/api'
};
config.production = {
    api_url: '//inapptranslation.com/api'
};
