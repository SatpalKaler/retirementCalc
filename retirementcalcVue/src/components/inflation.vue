<template>
    <div class="text-body-1">
      <p>
        {{ currency }}10,000 in 1993 ({{ yearsSince1993 }} years ago) could buy the same things as about
        <strong>{{ currency }}{{ Math.floor(10000 * Math.pow(1.03, yearsSince1993)).toLocaleString() }}</strong> today because
        prices have increased over {{ yearsSince1993 }} years due to inflation.
      </p>
      <p class="mt-4">
        For example, a burger that cost <strong>{{ currency }}5</strong> in 1993 now would cost
        <strong>{{currency}}{{ formatCurrency(currentBurgerCost) }}</strong>.
      </p>
      <p class="mt-5">Looking into the future:</p>
      <p class="mt-4">
        If you have <strong>{{ currency }}{{ formatCurrency(netWorth) }}</strong> in {{ yearsToRetirement }} years,
        it will buy as much as <strong>{{ currency }}{{ formatCurrency(realNetWorth) }}</strong> can today because
        money loses value over time.
      </p>
      <p class="mt-4">
        That means a burger costing <strong>{{ currency }}{{ formatCurrency(currentBurgerCost) }}</strong> today
        could cost <strong>{{currency}}{{ formatCurrency(futureBurgerCost) }}</strong> in {{ yearsToRetirement }} years.
      </p>
    </div>
  </template>
  
  <script setup>
  defineProps({
    yearsSince1993: Number,
    currentBurgerCost: Number,
    futureBurgerCost: Number,
    netWorth: Number,
    realNetWorth: Number,
    yearsToRetirement: Number,
    currency: String
  })
  
  const formatCurrency = (value) => {
    return value.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })
  }
  </script>