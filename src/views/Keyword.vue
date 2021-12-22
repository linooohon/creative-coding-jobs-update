<template>
  <div class="keyword_page">
    <div v-for="(jobItem, index) in jobData" :key="index" :job="job">
      <div v-for="item in Object.entries(jobItem)" :key="item[0]">
        <div class="keyword_page_keyword" v-bind="targetKeyword">
          <router-link :to="`/keyword/${item[0]}`">{{ item[0] }}</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Keyword',
  props: ['jobData']
}
</script>
