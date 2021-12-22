<template>
  <div class="jobCard_wrapper">
    <div v-for="(jobItem, index) in chunkData" :key="index">
      <div v-for="item in Object.entries(jobItem)" :key="item[0]">
        <div class="jobCard_keyword">{{ item[0] }}</div>
        <div class="jobCard_platform">
          <div class="jobCard_platform_linkedin">
            <div>{{ linkedin }}</div>
            <div v-for="(job, index) in item[1]" :key="`${job}_${index}`">
              <JobCard :job="job" :platform="linkedin" />
            </div>
          </div>
          <div class="jobCard_platform_glassdoor">
            <div>{{ glassdoor }}</div>
            <div v-for="(job, index) in item[1]" :key="`${job}_${index}`">
              <JobCard :job="job" :platform="glassdoor" />
            </div>
          </div>
          <div class="jobCard_platform_simplyhired">
            <div>{{ simplyhired }}</div>
            <div v-for="(job, index) in item[1]" :key="`${job}_${index}`">
              <JobCard :job="job" :platform="simplyhired" />
            </div>
          </div>
          <div class="jobCard_platform_indeed">
            <div>{{ indeed }}</div>
            <div v-for="(job, index) in item[1]" :key="`${job}_${index}`">
              <JobCard :job="job" :platform="indeed" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <button @click="loadData">More</button>
</template>

<script>
import JobCard from '@/components/JobCard.vue'

export default {
  name: 'Dashboard',
  data () {
    return {
      linkedin: 'LinkedIn',
      glassdoor: 'Glassdoor',
      simplyhired: 'SimplyHired',
      indeed: 'Indeed'
    }
  },
  props: ['chunkData', 'loadData'],
  components: {
    JobCard
  }
}
</script>
