<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Cookies</h1>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Cookie name</th>
              <th scope="col">Link</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(cookie, index) in cookies" :key="index">
              <td>{{ cookie.name }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" @click="handleClick(cookie.name)"
                  class="btn btn-warning btn-sm">Get ingredients
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Cookies',
  data() {
    return {
      cookies: [],
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:8888/cookies';
      axios.get(path)
        .then((res) => {
          this.cookies = res.data.cookies;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    handleClick(cookieName) {
      this.$router.push({ path: '/ingredients', query: { param: cookieName } });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
