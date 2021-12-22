<template>
  <div v-if="job.platform == platform">
    <a v-if="job.company_page_link != 'None'" :href="job.company_page_link">
      {{ job.company_name }}
    </a>
    <span v-else>{{ job.company_name }}</span>
    <span> | </span>
    <a v-if="job.job_page_link != 'None'" :href="job.job_page_link">
      {{ job.job_name }}
    </a>
    <span v-else>{{ job.job_name }}</span>
    <div>
      <span>{{ job.location }}</span>
      <span> | </span>
      <span>{{ job.update_time }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: ['job', 'platform']
}
</script>
