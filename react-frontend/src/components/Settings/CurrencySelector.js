import React from 'react'
import { DropdownButton, Dropdown } from 'react-bootstrap'
const currencyList = [
  'AED',
  'ARS',
  'AUD',
  'BCH',
  'BDT',
  'BHD',
  'BMD',
  'BNB',
  'BRL',
  'BTC',
  'CAD',
  'CHF',
  'CLP',
  'CNY',
  'CZK',
  'DKK',
  'DOT',
  'EOS',
  'ETH',
  'EUR',
  'GBP',
  'HKD',
  'HUF',
  'IDR',
  'ILS',
  'INR',
  'JPY',
  'KRW',
  'KWD',
  'LKR',
  'LTC',
  'MMK',
  'MXN',
  'MYR',
  'NGN',
  'NOK',
  'NZD',
  'PHP',
  'PKR',
  'PLN',
  'RUB',
  'SAR',
  'SEK',
  'SGD',
  'THB',
  'TRY',
  'TWD',
  'UAH',
  'USD',
  'VEF',
  'VND',
  'XAG',
  'XAU',
  'XDR',
  'XLM',
  'XRP',
  'YFI',
  'ZAR',
  'BITS',
  'LINK',
  'SATS'
]

function renderCurrencies () {
  const list = []
  for (const key in currencyList) {
    console.log(currencyList[key])
    list.push(<Dropdown.Item key={key}>{currencyList[key]}</Dropdown.Item>)
  }
  return list
}

function CurrencySelector () {
  return (
    <DropdownButton id="dropdown-basic-button" title="Currency">
      {renderCurrencies()}
    </DropdownButton>
  )
}

export default CurrencySelector
