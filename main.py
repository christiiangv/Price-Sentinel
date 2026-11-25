import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt, IntPrompt

from src.database import DatabaseManager
from src.scraper import PriceScraper
from src.analyzer import PriceAnalyzer
from src.notifier import TelegramNotifier

console = Console()
db = DatabaseManager()
scraper = PriceScraper()
analyzer = PriceAnalyzer()
notifier = TelegramNotifier()


def check_all_prices() -> None:
    products = db.get_all_products()
    if not products:
        console.print("[yellow]No hay productos registrados todavía.[/yellow]")
        return

    table = Table(title="📊 Reporte de Monitorización de Precios", show_lines=True)
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Producto", style="bold white")
    table.add_column("Actual", justify="right")
    table.add_column("Objetivo", justify="right")
    table.add_column("Mín. Hist.", justify="right")
    table.add_column("Estado", justify="center")

    with console.status("[bold green]Consultando precios en tiempo real..."):
        for prod_id, name, url, target_price, selector in products:
            current_price = scraper.fetch_price(url, selector)
            if current_price is None:
                table.add_row(str(prod_id), name, "Error", f"{target_price:.2f} €", "-", "[red]Sin acceso[/red]")
                continue

            history = db.get_price_history(prod_id)
            analysis = analyzer.analyze(current_price, history, target_price)
            db.record_price(prod_id, current_price)

            if analysis.is_target_reached:
                status = "[bold green]¡OFERTA![/bold green]"
                notifier.send_alert(name, url, analysis)
            else:
                status = "[dim]En seguimiento[/dim]"

            table.add_row(
                str(prod_id),
                name,
                f"{current_price:.2f} €",
                f"{target_price:.2f} €",
                f"{analysis.min_price:.2f} €",
                status,
            )

    console.print(table)


def add_new_product() -> None:
    console.print(Panel("➕ [bold]Añadir nuevo producto al rastreador[/bold]", expand=False))
    name = Prompt.ask("Nombre del producto")
    url = Prompt.ask("URL completa del producto")
    target = FloatPrompt.ask("Precio objetivo (€)")
    selector = Prompt.ask("Selector CSS del precio (ej. .price-tag, #priceblock)")

    try:
        prod_id = db.add_product(name, url, target, selector)
        console.print(f"[green]✔ Producto registrado con ID #{prod_id}[/green]")
    except Exception as e:
        console.print(f"[red]Error al guardar el producto: {e}[/red]")


def remove_product() -> None:
    prod_id = IntPrompt.ask("Introduce el ID del producto a eliminar")
    if db.delete_product(prod_id):
        console.print(f"[green]✔ Producto #{prod_id} eliminado.[/green]")
    else:
        console.print("[yellow]No se encontró ningún producto con ese ID.[/yellow]")


def menu() -> None:
    while True:
        console.print("\n[bold cyan]=== 🛡️ PriceSentinel CLI ===[/bold cyan]")
        console.print("1. Comprobar todos los precios ahora")
        console.print("2. Añadir producto")
        console.print("3. Eliminar producto")
        console.print("4. Salir")

        choice = Prompt.ask("Selecciona una opción", choices=["1", "2", "3", "4"], default="1")
        if choice == "1":
            check_all_prices()
        elif choice == "2":
            add_new_product()
        elif choice == "3":
            remove_product()
        elif choice == "4":
            break


if __name__ == "__main__":
    if "--check" in sys.argv:
        check_all_prices()
    else:
        menu()
