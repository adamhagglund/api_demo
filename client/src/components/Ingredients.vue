<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1 class="text-center">Ingredients for {{ this.$route.query.param }}</h1>
        <!-- <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add Book</button>
        <br><br> -->
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Amount</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(cookie, index) in ingredients" :key="index">
              <td>{{ cookie.ingredient }}</td>
              <td>{{ cookie.quantity + " " + cookie.unit }}</td>
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
  name: 'Ingredients',
  data() {
    return {
      ingredients: [],
    };
  },
  methods: {
    getMessage() {
      // eslint-disable-next-line
      const path = 'http://localhost:8888/frecipes\?cookie\='+this.$route.query.param;;
      axios.get(path)
        .then((res) => {
          this.ingredients = res.data.ingredients;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
