<template>
  <div>
    <ingredients/>
  </div>
</template>

<script>
// @ is an alias to /src
import Ingredients from '@/components/Ingredients.vue';

export default {
  name: 'TheIngredients',
  components: {
    Ingredients,
  },
};
</script>
