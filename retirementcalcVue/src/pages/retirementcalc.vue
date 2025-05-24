<template>
  <v-container>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="10">
          <div class="d-flex align-center justify-space-between mb-6">
            <h1 class="text-h2 font-weight-bold custom-title" style="font-family: 'Playfair Display', serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
              Retirement Calculator
            </h1>
            <v-switch
              v-model="isDark"
              :true-icon="'mdi-weather-night'"
              :false-icon="'mdi-weather-sunny'"
              :color="'teal'"
              label=""
              hide-details
              inset
              @change="toggleTheme"
            ></v-switch>
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
                  color="teal"
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
                  color="teal"
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
                  color="teal"
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
                  color="teal"
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
                  color="teal"
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
                  color="teal"
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
                  color="teal"
                />
              </v-col>
            </v-row>
          </v-card>
    
          <!-- Results Section -->
          <v-card class="mt-6 pa-6">
            <div class="text-h6 mb-8">Inflation-Adjusted Net Worth <span class="text-caption">(Real)</span></div>
            <div>
              <div :class="{'text-h1': $vuetify.display.mdAndUp, 'text-h2': $vuetify.display.mdAndDown}">
                <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedRealNetWorth) }}
                </span>
              </div>
              <div class="text-caption mt-8">
                Retirement Account: <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedRealFutureRetirementAccount) }}
                </span> • 
                Investments: <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedRealFutureInvestments) }}
                </span>
              </div>
            </div>

            <v-divider class="my-6"></v-divider>

            <div class="text-h6 mb-0" :class="{ 'greyed-out': isFinal }">Net Worth <span class="text-caption">(Nominal)</span></div>
            <div :class="{ 'greyed-out': isFinal }">
              <div class="text-h5">
                <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedNetWorth) }}
                </span>
              </div>
              <div class="text-caption mt-0">
                Retirement Account: <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedFutureRetirementAccount) }}
                </span> • 
                Investments: <span class="rolling-number" :class="{ 'final': isFinal }">
                  {{ formatCurrency(displayedFutureInvestments) }}
                </span>
              </div>
            </div>
          </v-card>

          <!-- Passive Income Calculator -->
          <v-card class="mt-6 pa-6">
            <div class="text-h6 mb-4">Passive Income Calculator</div>
            <p class="text-body-2 mb-4">
              Calculate how much monthly income your retirement savings could generate if invested in safe instruments.
            </p>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="passiveIncomeRate"
                  label="Annual Interest Rate (%)"
                  type="number"
                  variant="outlined"
                  density="compact"
                  min="0"
                  max="10"
                  step="0.1"
                  color="teal"
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="monthlyWithdrawal"
                  :label="`Monthly Withdrawal (${currency})`"
                  type="number"
                  variant="outlined"
                  density="compact"
                  color="teal"
                />
              </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <div class="d-flex flex-column flex-md-row justify-space-between align-start mb-4">
              <div class="mb-4 mb-md-0">
                <div class="text-subtitle-1 font-weight-bold">Monthly Interest Income</div>
                <div class="text-h4 mb-1">{{ formatCurrency(monthlyPassiveIncome) }}</div>
                <div class="text-caption">
                  Based on {{ passiveIncomeRate }}% annual return on {{ formatCurrency(realNetWorth) }}
                </div>
              </div>

              <div>
                <div class="text-subtitle-1 font-weight-bold">Principal Longevity</div>
                <div class="text-h4 mb-1" :class="{
                  'text-success': isPrincipalSustainable || principalYears > 30,
                  'text-warning': !isPrincipalSustainable && principalYears > 15,
                  'text-error': !isPrincipalSustainable && principalYears <= 15
                }">
                  {{ isPrincipalSustainable ? 'Indefinite' : `${principalYears} years` }}
                </div>
                <div class="text-caption">
                  {{ isPrincipalSustainable ? 'Your principal remains intact' : `Withdrawing ${formatCurrency(monthlyWithdrawal)} monthly` }}
                </div>
              </div>
            </div>

            <v-alert
              :type="isPrincipalSustainable ? 'success' : (principalYears > 20 ? 'info' : 'warning')"
              variant="tonal"
              density="compact"
            >
              {{ passiveIncomeMessage }}
            </v-alert>
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
              color="teal"
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
import { useTheme } from 'vuetify'


// Input fields
const currency = ref('RM')
const currentAge = ref(0)
const retirementAge = ref(0)
const currentRetirementAccount = ref(0)
const monthlyRetirementAccountContribution = ref(0)
const currentInvestments = ref(0)
const monthlyInvestments = ref(0)
const inputPanel = ref(0)
const passiveIncomeRate = ref(DEFAULT_PASSIVE_INCOME_RATE)
const monthlyWithdrawal = ref(0)
  
// Constants
const RetirementAccount_ANNUAL_RATE = 0.05
const INVESTMENT_ANNUAL_RATE = 0.10
const INFLATION_RATE = 0.03
const COMPOUNDING_FREQUENCY = 12
const DEFAULT_PASSIVE_INCOME_RATE = 4.0 // 4% default for safe investments
  
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

// Passive income calculations
const monthlyPassiveIncome = computed(() => {
  const annualRate = Number(passiveIncomeRate.value) / 100
  return (realNetWorth.value * annualRate) / 12
})

const isPrincipalSustainable = computed(() => {
  return monthlyPassiveIncome.value >= Number(monthlyWithdrawal.value) || Number(monthlyWithdrawal.value) === 0
})

const principalYears = computed(() => {
  if (isPrincipalSustainable.value || Number(monthlyWithdrawal.value) === 0) {
    return Infinity
  }
  
  const annualRate = Number(passiveIncomeRate.value) / 100
  const monthlyRate = annualRate / 12
  const principal = realNetWorth.value
  const withdrawal = Number(monthlyWithdrawal.value)
  
  // Calculate how many months the principal will last
  let remainingPrincipal = principal
  let months = 0
  
  while (remainingPrincipal > 0 && months < 1200) { // Cap at 100 years
    const interestEarned = remainingPrincipal * monthlyRate
    remainingPrincipal = remainingPrincipal + interestEarned - withdrawal
    months++
  }
  
  return Math.floor(months / 12)
})

const passiveIncomeMessage = computed(() => {
  if (isPrincipalSustainable.value) {
    return `Living off interest alone, you can withdraw up to ${formatCurrency(monthlyPassiveIncome.value)} monthly without depleting your principal.`
  } else if (principalYears.value > 30) {
    return `At your desired withdrawal rate of ${formatCurrency(monthlyWithdrawal.value)} monthly, your principal will last over 30 years.`
  } else {
    return `At your desired withdrawal rate of ${formatCurrency(monthlyWithdrawal.value)} monthly, your principal will be depleted in approximately ${principalYears.value} years.`
  }
})
  
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
  'Compounding frequency': 'Monthly',
  'Passive income default rate': '4%'
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
  [currentAge, retirementAge, currentRetirementAccount, monthlyRetirementAccountContribution, currentInvestments, monthlyInvestments, passiveIncomeRate, monthlyWithdrawal],
  () => {
    updateDisplayedValues()
  }
)

const showKofiModal = ref(false)

const theme = useTheme()
const isDark = ref(theme.global.current.value.dark)

const toggleTheme = () => {
  theme.global.name.value = isDark.value ? 'dark' : 'light'
}
</script>

<style scoped>
.rolling-number {
  display: inline-block;
  transition: all 0.5s ease-out;
}

.text-success {
  color: #4CAF50;
}

.text-warning {
  color: #FF9800;
}

.text-error {
  color: #F44336;
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


.v-switch {
  margin-left: auto;
}

@media (max-width: 600px) {
  .text-h2 {
    font-size: 1.75rem !important;
  }
}

.custom-title {
  position: relative;
  display: inline-block;
}

.custom-title::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #009688;
}

.greyed-out {
  opacity: 0.6;
  transition: opacity 0.5s ease-out;
}
</style>