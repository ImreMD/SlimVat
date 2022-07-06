import axios from  'axios';
import { useEffect} from "react";



export default function InvoiceItem(props) {

    const [listInvoice, setListInvoice] = [...props.manageList];

    useEffect( ()=> { console.log('Updated state', listInvoice)}, [listInvoice]);


    const selectItem = (invoice_nbr, checkedStatus) => {
    
        

        if (checkedStatus) {

            setListInvoice([...listInvoice, invoice_nbr])
            // setListInvoice((state) => {console.log(state); return state; });
            // console.log(getListInvoice()); 

        } else {

            setListInvoice([...listInvoice.filter(invoice => (invoice !== invoice_nbr))])
            // setListInvoice((state) => {console.log(state); return state; });

            
        }

        
        
            
    }

    const deleteToDoHandler = ({invoice_nbr}) => {
        
        axios.delete('http://localhost:8000/api/invoice/'+ invoice_nbr).then(res =>
        console.log(res.data))}
    return (

        <div>
            <div key={props.invoiceItem.invoice_nbr}>
                <label>
                    
                    <span style={{ fontWeight: 'bold, underline'}}> 
                        {props.invoiceItem.invoice_nbr} : {props.invoiceItem.description}
                    </span>
                    <span>
                        <input style = {{margin: '10px'}}
                                type='checkbox'
                                checked ={props.invoiceItem.status}
                                //key= {(props.invoiceItem.invoice_nbr.split("/")[1])}
                                onClick={(e) => {
                                    selectItem(props.invoiceItem.invoice_nbr, e.target.checked)
                                    
                                    }
                            }
                                value= 'false'
                        ></input>
                    </span>
                </label>
                <hr></hr>
                

            </div>


        </div>



    )



    }