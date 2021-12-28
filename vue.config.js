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
