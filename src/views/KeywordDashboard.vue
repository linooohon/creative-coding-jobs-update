<template>
  <div class="jobCard_wrapper">
    <div class="jobCard_keyword">{{ targetKeyword }}</div>
    <div v-for="(jobItem, index) in jobData" :key="index">
      <div v-for="item in Object.entries(jobItem)" :key="item[0]">
        <div v-if="targetKeyword == item[0]" class="jobCard_platform">
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
</template>

<script>
import JobCard from '@/components/JobCard.vue'

export default {
  name: 'KeywordDashboard',
  props: ['jobData', 'targetKeyword'],
  data () {
    return {
      linkedin: 'LinkedIn',
      glassdoor: 'Glassdoor',
      simplyhired: 'SimplyHired',
      indeed: 'Indeed'
    }
  },
  components: {
    JobCard
  }
}
</script>
