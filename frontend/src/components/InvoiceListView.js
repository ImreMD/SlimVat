import InvoiceItem from "./InvoiceItem";
import { useState} from "react";



export default function InvoiceViewList(props) {

    const [listInvoice, setListInvoice] = useState([]);
   

    return (
        
        <div>
            <ul>
                { props.invoiceList.map( invoice => 
                <InvoiceItem invoiceItem={invoice} 
                            manageList={[listInvoice, setListInvoice]}
                            /> 
                    ) }
            </ul>
        </div>
    )

}