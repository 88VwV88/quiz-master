import Vuex from 'vuex'

export const store = new Vuex.Store({
  state: {
    currentUser: null,
    authenticated: false,
    activeQuiz: null,
    quizzes: [],
    subjects: [],
    scores: [],
  },
  actions: {
    async loginUser({ commit }, data) {
      const currentUser = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .catch((error) => {
          console.error('[ERROR]', error)
        })

      commit('setAuthentication', {
        currentUser,
        authenticated: true,
      })
    },
    async fetchSubjects({ commit, state }) {
      if (state.currentUser != null) {
        const { subjects } = await fetch('http://localhost:5000/subjects', {
          headers: {
            Authorization: `Bearer ${state.currentUser.token}`,
          },
        })
          .then((response) => response.json())
          .catch((error) => {
            console.error('[ERROR]:', error)
          })

        commit('setSubjects', subjects)
      } else console.warn('USER LOGIN REQUIRED')
    },
    async fetchQuizzes({ commit, state }) {
      if (state.currentUser != null) {
        const { quizzes } = await fetch('http://localhost:5000/quizzes', {
          headers: {
            Authorization: `Bearer ${state.currentUser.token}`,
          },
        })
          .then((response) => response.json())
          .catch((error) => {
            console.error('[ERROR]:', error)
          })
        commit('setQuizzes', quizzes)
      } else console.warn('USER LOGIN REQUIRED')
    },
    async fetchScores({ commit, state }) {
      if (state.currentUser != null) {
        const { scores } = await fetch('http://localhost:5000/scores', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${state.currentUser.token}`,
          },
        })
          .then((response) => response.json())
          .catch((error) => console.error(error))
        commit('setScores', scores)
      } else console.warn('USER LOGIN REQUIRED')
    },
  },
  mutations: {
    setAuthentication(state, { currentUser, authenticated }) {
      state.currentUser = currentUser
      state.authenticated = authenticated
    },
    setQuizzes(state, quizzes) {
      state.quizzes = quizzes
    },
    setSubjects(state, subjects) {
      state.subjects = subjects
    },
    logoutUser(state) {
      state.currentUser = null
    },
    startQuiz(state, quizId) {
      state.activeQuiz = quizId
    },
    setScores(state, scores) {
      state.scores = scores
    },
  },
})
