
import './App.css';

import React,{useState, useEffect} from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css'
import InvoiceViewList from './components/InvoiceListView';

function App() {

  const [invoiceList, setInvoiceList]= useState([{}])
  const [invoice_nbr, setInvoice_nbr] = useState('')
  const [desc, setDesc] = useState('')
  const [cust, setCust] = useState('')
  const [vat, setVat] = useState(false)

  //Read all invoices
  useEffect( ()=> {
     axios.get('http://localhost:8000/api/invoices')
     .then(res => {  
       //console.log(res.data) 
       setInvoiceList(res.data);
     })
   });

  //Create an invoice
  const addTodoHandler = () => {
    axios.post('http://localhost:8000/api/invoice', {'invoice_nbr': invoice_nbr,
  'description': desc, 'customer': cust, 'vat_status': vat})
  .then( res => console.log(res
    ))
  };

  return (
    <div className='App list-group-item justify-content-center
      align-items-center mx-auto' style={{"width":"400px",
      "backgroundColor":"white", "marginTop":"15px"}}>

      <h1 className='card text-white bg-primary mb-1'
      stylename='max-width: 20rem;'> List Manager</h1>

      <h6 className='card text-white bg-primary mb-3'> FASTAPI - React
      - MongoDB </h6>

      <div className='card-body'>
        <h5 className='card text-white bg-dark mb-3'> Add your Invoice</h5>
        <span className='card-text'>

          <input className='mb-2 form-control titleIn' onChange= {event => 
          setInvoice_nbr(event.target.value)} placeholder='Invoice_nbr'/>

          <input className='mb-2 form-control desIn' onChange= {event => 
          setDesc(event.target.value)} placeholder='Description'/>

          <input className='mb-2 form-control desIn' onChange= {event => 
          setCust(event.target.value)} placeholder='Customer'/>

          <input className='mb-2 form-control desIn' onChange= {event => 
          setVat(event.target.value)} placeholder='VAT'/>



          <button className='btn btn-outline-primary mx-2 mb-3' style={{
            'borderRadius':'50 px', 'fontWeight':'bold'}} onClick=
            {addTodoHandler}> Add Invoice</button>
                 
        </span>
        <h5 className='card text-white bg-dark mb-3'> Your Tasks</h5>
      </div>

      <div>
            {/*  listofinvoices */}
        <InvoiceViewList invoiceList= {invoiceList} /> 
            
      </div>
    </div>
  
  );
}

export default App;