<template>
  <div class="search">
    <p>search page</p>
    <input type="text" v-model="searchQuery">
    <button @click="searchHandler(searchQuery)">enter</button>
  </div>
</template>

<script>
export default {
  name: 'Search',
  data () {
    return {
      searchQuery: ''
    }
  },
  methods: {
    searchHandler (searchQuery) {
      this.$router.push(
        {
          name: 'SearchDashboard',
          params: { searchQuery }
        }
      )
      console.log(searchQuery)
    }
  }
}
</script>
