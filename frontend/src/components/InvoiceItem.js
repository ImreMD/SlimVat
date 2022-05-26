import axios from  'axios';
import React from 'react';

export default function InvoiceItem(props) {

    const selectItem = (invoice_nbr) => {

        var selected = ""
        selected = "Selected invoices : " + invoice_nbr
        console.log(selected )
        

    }

    const deleteToDoHandler = (invoice_nbr) => {
        console.log(invoice_nbr)
        axios.delete('http://localhost:8000/api/invoice/'+ invoice_nbr).then(res =>
        console.log(res.data))}
    return (

        <div key={props.invoiceItem.invoice_nbr} onClick={() => selectItem(props.InvoiceItem.invoice_nbr)} >
            <div >
                <span style={{ fontWeight: 'bold, underline'}}> {props.invoiceItem.invoice_nbr} : {props.invoiceItem.description}
                <button onClick={() => deleteToDoHandler(props.invoiceItem.invoice_nbr) }
                className='btn btn-outline-danger my-2 mx-2' style={
                    {'borderRadius':'50px', } }> check </button>
                </span>
                <hr></hr>
                

            </div>


        </div>



    )



    }