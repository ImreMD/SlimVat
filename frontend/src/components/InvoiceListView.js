import InvoiceItem from "./InvoiceItem"

export default function InvoiceViewList(props) {
    return (
        <div>
            <ul>
                {props.invoiceList.map( invoice => < InvoiceItem invoiceItem={invoice} /> )}
            </ul>
        </div>
    )

}