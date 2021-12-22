import { createStore } from 'vuex'
import axios from 'axios'

// not use right now
export default createStore({
  state: {
    dataArray: [],
    updateTime: ''
  },
  mutations: {
    assignToData (state, payload) {
      state.dataArray = payload
    },
    assignUpdateTime (state, payload) {
      state.updateTime = payload
    }
  },
  actions: {
    async getTotalJobData (context) {
      const data = await axios.get('https://raw.githubusercontent.com/linooohon/creative-coding-jobs-update/main/data/final.json')
      context.commit('assignToData', data.data)
    },
    async getUpdateTime (context) {
      const data = await axios.get('https://raw.githubusercontent.com/linooohon/creative-coding-jobs-update/main/data/update_time.log')
      context.commit('assignUpdateTime', data.data)
    }
  },
  modules: {
  }
})
