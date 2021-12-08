export const initialCurrencyState = {
  currentCurrency: 'USD'
}

const CURRENCY_UPDATE = 'CURRENCY_UPDATE'

export const updateCurrency = (currency) => {
  return {
    type: CURRENCY_UPDATE,
    payload: [currency]
  }
}

export const currencyReducer = (state = initialCurrencyState, action) => {
  switch (action.type) {
    case CURRENCY_UPDATE:
      return {
        ...state,
        currentCurrency: action.payload[0]
      }

    default:
      return {
        ...state
      }
  }
}
