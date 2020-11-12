from django.shortcuts import render, redirect, get_object_or_404
from .forms import StockForm
from .models import Stock
from django.contrib import messages


# Create your views here.
# public api = pk_0f0f0aa8153046e2847d2c60fdc4209d

def home(request):
    import requests
    import json

    if request.method == "POST":
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_0f0f0aa8153046e2847d2c60fdc4209d")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'quotes/home.html', {'api': api})
    else:
        return render(request, 'quotes/home.html', {'ticker': "Please enter a ticker symbol above"})


def about(request):
    data = {}
    return render(request, 'quotes/about.html', data)


def add_stock(request):
    import requests
    import json

    if request.method == "POST":
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added")
            return redirect('add_stock')
    else:
        tickers = Stock.objects.all()
        output = []
        for ticker in tickers:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker) + "/quote?token=pk_0f0f0aa8153046e2847d2c60fdc4209d")
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."
        data = {'tickers': tickers, 'output': output}
        return render(request, 'quotes/add_stock.html', data)


def delete(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, "Stock has been deleted")
        return redirect('add_stock')


def deletestock(request):
    tickers = Stock.objects.all()
    data = {'tickers': tickers}
    return render(request, 'quotes/delete_stock.html', data)