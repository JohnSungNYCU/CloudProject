export default {
    namespaced: true,
    state: {
      uploadedFileName: localStorage.getItem('uploadedFileName') || null
    },
    mutations: {
      setUploadedFileName(state, fileName) {
        state.uploadedFileName = fileName;
        localStorage.setItem('uploadedFileName', fileName);
      }
    },
    actions: {
      clearUploadedFileName({ commit }) {
        commit('setUploadedFileName', null);
        localStorage.removeItem('uploadedFileName');
      }
    }
  }