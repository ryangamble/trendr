import React, { useState } from 'react'
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

function CurrencySelector () {
  const [currency, setCurrency] = useState()

  function renderCurrencies () {
    const list = []
    for (const key in currencyList) {
      // console.log(currencyList[key])
      list.push(<Dropdown.Item key={key} eventKey={currencyList[key]}>{currencyList[key]}</Dropdown.Item>)
    }
    return list
  }

  // TODO: If logged in, fetch preferred currency from db and store in state

  // TODO: If logged in, update user currency in db
  const handleSelect = (e) => {
    console.log('changed currency to:', e)
    setCurrency(e)
  }

  return (
    <>
      <div style={{ color: 'black' }}>Currency</div>
      <DropdownButton
        id="dropdown-basic-button"
        title={currency || 'Select Currency'}
        onSelect={handleSelect}
      >
        <div style={{ overflowY: 'scroll', height: '50vh' }}>
        {renderCurrencies()}
        </div>
      </DropdownButton>
    </>
  )
}

export default CurrencySelector
