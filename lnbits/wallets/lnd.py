from requests import Response, get, post
from flask import jsonify
from .base import InvoiceResponse, TxStatus, Wallet, PaymentResponse
import json


class LndWallet(Wallet):
    """https://api.lightning.community/rest/index.html#lnd-rest-api-reference"""

    def __init__(self, *, endpoint: str, admin_macaroon: str, invoice_macaroon: str, read_macaroon: str):
        self.endpoint = endpoint[:-1] if endpoint.endswith("/") else endpoint
        self.auth_admin = {"Grpc-Metadata-macaroon": admin_macaroon}
        self.auth_invoice = {"Grpc-Metadata-macaroon": invoice_macaroon}
        self.auth_read = {"Grpc-Metadata-macaroon": read_macaroon}

    def create_invoice(self, amount: int, memo: str = "") -> InvoiceResponse:
        payment_hash, payment_request = None, None
        r = post(
            url=f"{self.endpoint}/v1/invoices",
            headers=self.auth_admin,
            json={"value": "100", "memo": memo, "private": True},  # , "private": True},
        )

        if r.ok:
            data = r.json()
            payment_request = data["payment_request"]

        rr = get(url=f"{self.endpoint}/v1/payreq/{payment_request}", headers=self.auth_read)
        print(rr.json())
        if rr.ok:
            dataa = rr.json()
            payment_hash = dataa["payment_hash"]


        return InvoiceResponse(r, payment_hash, payment_request)



    def pay_invoice(self, bolt11: str) -> PaymentResponse:
        fee_msat = None
        r = post(url=f"{self.endpoint}/v1/channels/transactions", headers=self.auth_admin, json={"payment_request": bolt11})
        return PaymentResponse(r)



    def get_invoice_status(self, payment_hash: str, wait: bool = True) -> TxStatus:
        r = get(url=f"{self.endpoint}/v1/invoice/{payment_hash}", headers=self.auth_read)
    #    print(payment_hash)
        print(r.json())
        if not r.ok:
            return TxStatus(r, None)

        return TxStatus(r, r.json()["settled"])

    def get_payment_status(self, payment_hash: str) -> TxStatus:
        r = get(url=f"{self.endpoint}/v1/payments", headers=self.auth_admin, params={"include_incomplete": True})

        if not r.ok:
            return TxStatus(r, None)

        payments = [p for p in r.json()["payments"] if p["payment_hash"] == payment_hash]
        payment = payments[0] if payments else None

        # check payment.status: https://api.lightning.community/rest/index.html?python#peersynctype
        statuses = {"UNKNOWN": None, "IN_FLIGHT": None, "SUCCEEDED": True, "FAILED": False}
        return TxStatus(r, statuses[payment["status"]] if payment else None)


