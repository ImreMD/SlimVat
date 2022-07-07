import InvoiceItem from "./InvoiceItem";
import { useState} from "react";
import axios from 'axios';


export default function InvoiceViewList(props) {
//list of selected invoices
//create a function to send invoices to backend where the status will be modified

    const [listInvoice, setListInvoice] = useState([]);
    
    const sendModifications = () => {
          axios.put('http://localhost:8000/api/invoices', {invoices_send: listInvoice})
    //   'description': desc, 'customer': cust, 'vat_status': vat})
      .then( res => console.log(res.data
         ))

        console.log(listInvoice)
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
                <InvoiceItem invoiceItem={invoice} manageList={[listInvoice, setListInvoice]}
                            /> 
                    ) }
            </ul>
        </div>
    )

}