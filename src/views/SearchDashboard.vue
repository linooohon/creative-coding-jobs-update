<template>
  <div class="jobCard_wrapper">
    <p>Search: "{{ searchQuery }}", if the result is blank, means no result for this keyword.</p>
    <div v-for="(jobItem, index) in jobData" :key="index">
      <div v-for="item in Object.entries(jobItem)" :key="item[0]">
        <!-- <div class="jobCard_keyword">{{ item[0] }}</div> -->
        <div
          class="jobCard_platform"
        >
          <!-- <div class="jobCard_platform_linkedin">
            <div>{{ linkedin }}</div>
            <div v-for="(job, index) in item[1]" :key="`${job}_${index}`">
              <JobCard :job="job" :platform="linkedin" v-if="job.company_name.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1 || job.job_name.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1"/>
            </div>
          </div> -->
          <div class="jobCard_platform_glassdoor">
            <!-- <div>{{ glassdoor }}</div> -->
            <div v-for="(job, index) in item[1]" :key="`${job}_${index}`">
              <JobCard :job="job" :platform="glassdoor" v-if="job.company_name.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1 || job.job_name.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1"/>
            </div>
          </div>
          <div class="jobCard_platform_simplyhired">
            <!-- <div>{{ simplyhired }}</div> -->
            <div v-for="(job, index) in item[1]" :key="`${job}_${index}`">
              <JobCard :job="job" :platform="simplyhired" v-if="job.company_name.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1 || job.job_name.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1"/>
            </div>
          </div>
          <div class="jobCard_platform_indeed">
            <!-- <div>{{ indeed }}</div> -->
            <div v-for="(job, index) in item[1]" :key="`${job}_${index}`">
              <JobCard :job="job" :platform="indeed" v-if="job.company_name.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1 || job.job_name.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1"/>
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
  name: 'SearchDashboard',
  props: ['jobData', 'searchQuery'],
  data () {
    return {
      // linkedin: 'LinkedIn',
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
