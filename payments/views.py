from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from .forms import PaymentForm

def payment_page(request, pk=None):
    payment = None
    if pk:
        payment = get_object_or_404(Payment, pk=pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment-page')
    else:
        form = PaymentForm(instance=payment)

    payments = Payment.objects.all().order_by('-id')

    return render(request, 'payments/payment_page.html', {
        'form': form,
        'payments': payments,
        'edit_id': pk
    })

def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    payment.delete()
    return redirect('payment-page')