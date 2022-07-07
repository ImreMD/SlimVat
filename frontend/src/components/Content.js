import InvoiceItem from "./InvoiceItem";
import { useState} from "react";
import axios from 'axios';


export default function Content(props) {

    const [listInvoice, setListInvoice] = useState([]);
    const selectItem = (invoice_nbr, checkedStatus) => {
        if (checkedStatus) {

            setListInvoice([...listInvoice, invoice_nbr])
            
        } else {

            setListInvoice([...listInvoice.filter(invoice => (invoice !== invoice_nbr))])
            
        }     
    };

//list of selected invoices
//create a function to send invoices to backend where the status will be modified

    
    
    const sendModifications = () => {
          axios.put('http://localhost:8000/api/invoices', {invoices_send: listInvoice})
    //   'description': desc, 'customer': cust, 'vat_status': vat})
      .then( res => console.log(res.data
         ))

        console.log(listInvoice)
      };

    const handleCheck= (invoice_nbr) =>{
        const listItems = props.invoiceList.map((item) => item.invoice_nbr === invoice_nbr ? {...item,
        vat_status:!item.vat_status} : item);
        props.setInvoiceList(listItems);

    };

    return (
        
        <div>
            <div> 
                {listInvoice}
                <button className='btn btn-outline-primary mx-2 mb-3' style={{
                'borderRadius':'50 px', 'fontWeight':'bold'}} onClick=
                {sendModifications}> Snd Modifications</button> 
            </div>
            <ul>
                { props.invoiceList.map( invoice => 
                <InvoiceItem    invoiceItem={invoice} 
                                manageList={[listInvoice, setListInvoice]}
                                selectItem = {selectItem}
                                handleCheck={handleCheck}
                            /> 
                    ) }
            </ul>
        </div>
    )

}