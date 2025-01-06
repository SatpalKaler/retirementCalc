<template>
  <v-container>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10">
          <div class="d-flex align-center justify-space-between mb-6">
            <h1 class="text-h2 font-weight-bold" style="font-family: 'Playfair Display', serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
              Retirement Calculator
            </h1>
          </div>

          <!-- Input Section -->
          <v-card class="pa-6 mb-6">
            <v-row>
              <v-col cols="12" md="2">
                <v-text-field
                  v-model="currency"
                  label="Currency"
                  variant="outlined"
                  density="compact"
                />
              </v-col>
              <v-col cols="12" md="5">
                <v-text-field
                  v-model="currentAge"
                  label="Current Age"
                  type="number"
                  variant="outlined"
                  density="compact"
                  min="0"
                  max="100"
                />
              </v-col>
              <v-col cols="12" md="5">
                <v-text-field
                  v-model="retirementAge"
                  label="Expected Age of Retirement"
                  type="number"
                  variant="outlined"
                  density="compact"
                  min="0"
                  max="100"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="currentRetirementAccount"
                  :label="`Current Retirement Account (${currency})`"
                  prefix="🏦"
                  variant="outlined"
                  density="compact"
                />
              </v-col>
            <v-col cols="12" md="6">
                <v-text-field
                  v-model="monthlyRetirementAccountContribution"
                  :label="`Monthly Retirement Account Contribution (${currency})`"
                  prefix="🏦"
                  variant="outlined"
                  density="compact"
                  type="number"
                />
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="currentInvestments"
                  :label="`Current Investments (${currency})`"
                  prefix="📈"
                  variant="outlined"
                  density="compact"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="monthlyInvestments"
                  :label="`Monthly Investments (${currency})`"
                  prefix="📈"
                  variant="outlined"
                  density="compact"
                  type="number"
                />
              </v-col>
            </v-row>
          </v-card>
    
          <!-- Results Section -->
          <v-card class="mt-6 pa-6">
            <div class="text-h6 mb-4">Net Worth by Retirement <span class="text-caption">(Nominal)</span></div>
            <div>
              <div class="text-h2">
                <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedNetWorth) }}
                </span>
              </div>
              <div class="text-caption mt-2">
                Retirement Account: <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedFutureRetirementAccount) }}
                </span> • 
                Investments: <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedFutureInvestments) }}
                </span>
              </div>
            </div>

            <v-divider class="my-6"></v-divider>

            <div class="text-h6 mb-4">Inflation-Adjusted Net Worth</div>
            <div>
              <div class="text-h2">
                <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedRealNetWorth) }}
                </span>
              </div>
              <div class="text-caption mt-2">
                Retirement Account: <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedRealFutureRetirementAccount) }}
                </span> • 
                Investments: <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedRealFutureInvestments) }}
                </span>
              </div>
            </div>
          </v-card>
    
          <!-- Inflation Explanation -->
          <v-expansion-panels class="mt-6">
            <v-expansion-panel title="💡 How Inflation Works">
              <v-expansion-panel-text>
                <InflationExplanation
                  :years-since-1993="yearsSince1993"
                  :current-burger-cost="currentBurgerCost"
                  :future-burger-cost="futureBurgerCost"
                  :net-worth="netWorthByRetirement"
                  :real-net-worth="realNetWorth"
                  :years-to-retirement="yearsToRetirement"
                  :currency="currency"
                />
              </v-expansion-panel-text>
            </v-expansion-panel>

            <!-- New Information Panel -->
            <v-expansion-panel title="ℹ️ Assumptions & Formulas">
              <v-expansion-panel-text>
                <v-container class="px-4 py-2">
                  <div class="text-subtitle-1 font-weight-bold mb-2">Disclaimer:</div>
                  <p class="text-body-2 mb-4">
                    This calculator provides an estimate based on the inputs and assumptions provided. Actual results may vary. <br><br> Please don't hunt me down in {{ yearsToRetirement }} years.
                  </p>

                  <v-divider class="mb-4"></v-divider>

                  <div class="text-subtitle-1 font-weight-bold mb-2">Assumptions:</div>
                  <v-list density="compact" class="mb-4">
                    <v-list-item v-for="(value, label) in assumptions" :key="label">
                      <template v-slot:title>
                        <span class="text-body-2">{{ label }}: {{ value }}</span>
                      </template>
                    </v-list-item>
                  </v-list>

                  <v-divider class="mb-4"></v-divider>

                  <div class="text-subtitle-1 font-weight-bold mb-2">Formulas:</div>
                  
                  <div class="mb-4">
                    <div class="text-body-2 font-weight-bold">Future Value (FV):</div>
                    <v-card class="bg-grey-lighten-4 pa-2 my-2">
                      <code class="text-body-2">A = P(1 + r/n)^(nt) + PMT((1 + r/n)^(nt) - 1)/(r/n)</code>
                    </v-card>
                    <div class="text-body-2">
                      Where:<br>
                      P = Present Value<br>
                      r = Annual Interest Rate<br>
                      n = Number of Compounding Periods per Year<br>
                      t = Number of Years<br>
                      PMT = Payment per Period
                    </div>
                  </div>

                  <div class="mb-4">
                    <div class="text-body-2 font-weight-bold">Inflation-Adjusted Value:</div>
                    <v-card class="bg-grey-lighten-4 pa-2 my-2">
                      <code class="text-body-2">FV_adjusted = PV * (1 + r)^t</code>
                    </v-card>
                    <div class="text-body-2">
                      Where:<br>
                      FV_adjusted = Future Value adjusted for inflation<br>
                      PV = Present Value<br>
                      r = Inflation Rate<br>
                      t = Number of Years
                    </div>
                  </div>

                  <v-divider class="mb-4"></v-divider>

                  <div class="text-subtitle-1 font-weight-bold mb-2">References:</div>
                  <v-list density="compact">
                    <v-list-item
                      v-for="(link, index) in references"
                      :key="index"
                      :href="link.url"
                      target="_blank"
                      :title="link.text"
                    >
                      <template v-slot:title>
                        <span class="text-body-2 text-primary">{{ link.text }}</span>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-container>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>

          <!-- Add Support section at bottom -->
          <div class="d-flex justify-center mt-6">
            <v-btn
              color="primary"
              @click="showKofiModal = true"
              prepend-icon="mdi-coffee"
              class="support-btn"
            >
              Support this creator
            </v-btn>
          </div>

          <KofiModal
            v-model="showKofiModal"
            @close="showKofiModal = false"
          />
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>
  
<script setup>
import { ref, computed, watch } from 'vue'
import { debounce } from 'lodash'
import InflationExplanation from '@/components/inflation.vue'
import KofiModal from '@/components/KofiModal.vue'


// Input fields
const currency = ref('RM')
const currentAge = ref(0)
const retirementAge = ref(0)
const currentRetirementAccount = ref(0)
const monthlyRetirementAccountContribution = ref(0)
const currentInvestments = ref(0)
const monthlyInvestments = ref(0)
const inputPanel = ref(0)
  
// Constants
const RetirementAccount_ANNUAL_RATE = 0.05
const INVESTMENT_ANNUAL_RATE = 0.10
const INFLATION_RATE = 0.03
const COMPOUNDING_FREQUENCY = 12
  
// Computed values
const yearsToRetirement = computed(() => retirementAge.value - currentAge.value)
  
const yearsSince1993 = computed(() => new Date().getFullYear() - 1993)
  
// Calculate future values
const calculateFutureValue = (P, r, n, t, PMT) => {
  return P * Math.pow(1 + r/n, n*t) + PMT * ((Math.pow(1 + r/n, n*t) - 1) / (r/n))
}
  
const futureRetirementAccount = computed(() => {
  return calculateFutureValue(
    Number(currentRetirementAccount.value),
    RetirementAccount_ANNUAL_RATE,
    COMPOUNDING_FREQUENCY,
    yearsToRetirement.value,
    monthlyRetirementAccountContribution.value
  )
})
  
const futureInvestments = computed(() => {
  return calculateFutureValue(
    Number(currentInvestments.value),
    INVESTMENT_ANNUAL_RATE,
    COMPOUNDING_FREQUENCY,
    yearsToRetirement.value,
    monthlyInvestments.value
  )
})
  
const netWorthByRetirement = computed(() => futureRetirementAccount.value + futureInvestments.value)
  
// Inflation adjusted values
const realFutureRetirementAccount = computed(() => 
  futureRetirementAccount.value / Math.pow(1 + INFLATION_RATE, yearsToRetirement.value)
)
  
const realFutureInvestments = computed(() => 
  futureInvestments.value / Math.pow(1 + INFLATION_RATE, yearsToRetirement.value)
)
  
const realNetWorth = computed(() => realFutureRetirementAccount.value + realFutureInvestments.value)
  
// Burger cost calculations
const INITIAL_BURGER_COST_1993 = 5.00
const currentBurgerCost = computed(() => 
  INITIAL_BURGER_COST_1993 * Math.pow(1 + INFLATION_RATE, yearsSince1993.value)
)
const futureBurgerCost = computed(() => 
  currentBurgerCost.value * Math.pow(1 + INFLATION_RATE, yearsToRetirement.value)
)
  
// Formatting helper
const formatCurrency = (value) => {
  return `${currency.value}${value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}`
}
  
const assumptions = {
  'Retirement Account annual return': '5%',
  'Investment annual return': '10%',
  'Inflation rate (past & future)': '3%',
  'Compounding frequency': 'Monthly'
}
  
const references = [
  {
    text: 'CPI Inflation Calculator',
    url: 'https://www.dosm.gov.my/cpi_calc/index.php'
  },
  {
    text: 'Compound Interest Calculator',
    url: 'https://www.thecalculatorsite.com/finance/calculators/compound-interest-formula'
  },
  {
    text: 'Compound Interest - Wikipedia',
    url: 'https://en.wikipedia.org/wiki/Compound_interest'
  },
  {
    text: 'Future Value - Wikipedia',
    url: 'https://en.wikipedia.org/wiki/Future_value'
  }
]
  
// Add new refs for displayed results
const displayedNetWorth = ref(0)
const displayedFutureRetirementAccount = ref(0)
const displayedFutureInvestments = ref(0)
const displayedRealNetWorth = ref(0)
const displayedRealFutureRetirementAccount = ref(0)
const displayedRealFutureInvestments = ref(0)
const isLoading = ref(false)
  
// Add refs to track final state
const isFinal = ref(false)
  
// Add this function to generate random numbers within a range
const getRandomNumber = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1)) + min
}
  
// Modify the updateDisplayedValues function
const updateDisplayedValues = debounce(() => {
  isLoading.value = true
  isFinal.value = false // Reset final state
  
  const animationDuration = 2000
  const intervalTime = 50
  const steps = animationDuration / intervalTime
  let currentStep = 0
  
  const interval = setInterval(() => {
    currentStep++
    
    const progress = currentStep / steps
    const randomFactor = 1 - progress
    
    // Update displayed values...
    displayedNetWorth.value = netWorthByRetirement.value * (1 + (Math.random() - 0.5) * randomFactor)
    displayedFutureRetirementAccount.value = futureRetirementAccount.value * (1 + (Math.random() - 0.5) * randomFactor)
    displayedFutureInvestments.value = futureInvestments.value * (1 + (Math.random() - 0.5) * randomFactor)
    displayedRealNetWorth.value = realNetWorth.value * (1 + (Math.random() - 0.5) * randomFactor)
    displayedRealFutureRetirementAccount.value = realFutureRetirementAccount.value * (1 + (Math.random() - 0.5) * randomFactor)
    displayedRealFutureInvestments.value = realFutureInvestments.value * (1 + (Math.random() - 0.5) * randomFactor)
    
    if (currentStep >= steps) {
      // Set final values
      displayedNetWorth.value = netWorthByRetirement.value
      displayedFutureRetirementAccount.value = futureRetirementAccount.value
      displayedFutureInvestments.value = futureInvestments.value
      displayedRealNetWorth.value = realNetWorth.value
      displayedRealFutureRetirementAccount.value = realFutureRetirementAccount.value
      displayedRealFutureInvestments.value = realFutureInvestments.value
      isLoading.value = false
      isFinal.value = true // Trigger final state
      clearInterval(interval)
    }
  }, intervalTime)
}, 500)
  
// Watch for changes in input values
watch(
  [currentAge, retirementAge, currentRetirementAccount, monthlyRetirementAccountContribution, currentInvestments, monthlyInvestments],
  () => {
    updateDisplayedValues()
  }
)

const showKofiModal = ref(false)
</script>

<style scoped>
.rolling-number {
  display: inline-block;
  transition: all 0.5s ease-out;
}

.rolling-number.final {
  color: #4DB6AC;
  font-weight: bold;
  transform: scale(1.02);
  animation: popFinal 0.5s ease-out;
}

@keyframes popFinal {
  0% {
    transform: scale(1);
    color: inherit;
  }
  50% {
    transform: scale(1.06);
    color: #4DB6AC;
  }
  100% {
    transform: scale(1.04);
    color: #4DB6AC;
  }
}

/* Optional: Add a subtle glow effect */
.rolling-number.final {
  text-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
}
</style>