<template>
  <div id="nav">
    <router-link to="/">Dashboard</router-link> |
    <router-link to="/keyword">Keyword</router-link> |
    <router-link to="/search">Search</router-link>
  </div>
  <router-view :jobData="totalJobData"/>
</template>

<script>
import ccJob from './final.json'
export default {
  data () {
    return {
      totalJobData: ccJob
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
