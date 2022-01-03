// References: deploy on github pages and netlify
// https://cli.vuejs.org/guide/deployment.html#netlify

module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/creative-coding-jobs-update/'
    : '/'
}

module.exports = {
  pwa: {
    workboxOptions: {
      exclude: [/_redirects/]
    }
  }
}

module.exports = {
  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = 'Creative Coding Jobs Daily Update'
      return args
    })
  }
}
