import { createStore } from 'vuex'
import axios from 'axios'

// not use right now
export default createStore({
  state: {
    dataArray: []
  },
  mutations: {
    assignToData (state, payload) {
      state.dataArray = payload
    }
  },
  actions: {
    async getTotalJobData (context) {
      const data = await axios.get('https://raw.githubusercontent.com/linooohon/creative-coding-jobs-update/main/src/final.json')
      context.commit('assignToData', data.data)
    }
  },
  modules: {
  }
})
