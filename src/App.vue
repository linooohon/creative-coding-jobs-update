<template>
  <div id="nav">
    <router-link to="/">Dashboard</router-link> |
    <router-link to="/keyword">Keyword</router-link> |
    <router-link to="/search">Search</router-link>
    <p>Update at: {{ updateTime }}</p>
  </div>
  <router-view :chunkData="chunkJobData" :jobData="totalJobData" :loadData="loadData"/>
</template>

<script>
// import ccJob from './final.json'
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  data () {
    return {
      totalJobData: [], // no vuex
      keywordChunk: 3
    }
  },
  mounted () {
    this.getTotalJobData()
    this.getUpdateTime()
  },
  computed: {
    chunkJobData () {
      if (this.keywordChunk > this.totalJobData.length) {
        return this.totalJobData
      }
      return this.totalJobData.slice(0, this.keywordChunk)
    },
    ...mapState(['updateTime'])
  },
  methods: {
    // no vuex
    getTotalJobData () {
      axios.get('https://raw.githubusercontent.com/linooohon/creative-coding-jobs-update/main/data/static/final.json').then((res) => {
        this.totalJobData = res.data
      })
    },
    getUpdateTime () {
      this.$store.dispatch('getUpdateTime')
    },
    loadData () {
      this.keywordChunk += 3
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
  color: rgb(62, 171, 184);
}
</style>
