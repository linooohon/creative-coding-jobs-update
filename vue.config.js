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
