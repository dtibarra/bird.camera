export default routes => ({
  name: 'forward-to-trailing-slash',
  configureServer(server) {
      server.middlewares.use((req, _res, next) => {
          const requestURLwithoutLeadingSlash = req.url.substring(1)
          if (routes.includes(requestURLwithoutLeadingSlash)) {
              req.url = `${req.url}/`
          }
          next()
      })
  }
})