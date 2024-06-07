export default {
  namespaced: true,
  state: {
    uploadedFileName: localStorage.getItem('uploadedFileName') || null,
    uploadedFileUrl: localStorage.getItem('uploadedFileUrl') || null
  },
  mutations: {
    setUploadedFile(state, { name, url }) {
      state.uploadedFileName = name;
      state.uploadedFileUrl = url;
      localStorage.setItem('uploadedFileName', name);
      localStorage.setItem('uploadedFileUrl', url);
    },
    clearUploadedFile(state) {
      state.uploadedFileName = null;
      state.uploadedFileUrl = null;
      localStorage.removeItem('uploadedFileName');
      localStorage.removeItem('uploadedFileUrl');
    }
  },
  actions: {
    setUploadedFileInfo({ commit }, { name, url }) {
      commit('setUploadedFile', { name, url });
    },
    clearUploadedFileInfo({ commit }) {
      commit('clearUploadedFile');
    }
  }
}