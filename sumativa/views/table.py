import reflex as rx
from ..backend.backend import State, Customer
from ..components.form_field import form_field
from ..components.status_badges import status_badge


def show_customer(user: Customer):
    """Show a customer in a table row."""

    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.phone),
        rx.table.cell(user.address),
        rx.table.cell(f"${user.payments:,}"),
        rx.table.cell(user.date),
        rx.table.cell(
            rx.match(
                user.status,
                ("Entregado", status_badge("Entregado")),
                ("Pendiente", status_badge("Pendiente")),
                ("Cancelado", status_badge("Cancelado")),
                status_badge("Pendiente"),
            )
        ),
        rx.table.cell(
            rx.hstack(
                update_customer_dialog(user),
                rx.icon_button(
                    rx.icon("trash-2", size=22),
                    on_click=lambda: State.delete_customer(getattr(user, "id")),
                    size="2",
                    variant="solid",
                    color_scheme="red",
                ),
            )
        ),
        style={"_hover": {"bg": rx.color("gray", 3)}},
        align="center",
    )


def add_customer_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Añadir Cliente", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="users", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Añadir nuevo cliente",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Llena los campos para añadir un nuevo cliente",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Name
                        form_field(
                            "Nombre",
                            "Nombre del cliente",
                            "text",
                            "name",
                            "user",
                        ),
                        # Email
                        form_field(
                            "Correo", "user@reflex.dev", "email", "email", "mail"
                        ),
                        # Phone
                        form_field("Telefono", "Telefono del cliente", "tel", "phone", "phone"),
                        # Address
                        form_field(
                            "Dirección", "Dirección del cliente", "text", "address", "home"
                        ),
                        # Payments
                        form_field(
                            "Pago ($)",
                            "Pago del cliente",
                            "number",
                            "payments",
                            "dollar-sign",
                        ),
                        # Status
                        rx.vstack(
                            rx.hstack(
                                rx.icon("truck", size=16, stroke_width=1.5),
                                rx.text("Status"),
                                align="center",
                                spacing="2",
                            ),
                            rx.radio(
                                ["Entregado", "Pendiente", "Cancelado"],
                                name="status",
                                direction="row",
                                as_child=True,
                                required=True,
                            ),
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Agregar Cliente"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.add_customer_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def update_customer_dialog(user):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square-pen", size=22),
                rx.text("Editar", size="3"),
                color_scheme="blue",
                size="2",
                variant="solid",
                on_click=lambda: State.get_user(user),
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Editar Customer",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Editar la información del cliente",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Name
                        form_field(
                            "Nombre",
                            "Nombre del cliente",
                            "text",
                            "name",
                            "user",
                            user.name,
                        ),
                        # Email
                        form_field(
                            "Correo",
                            "user@reflex.dev",
                            "email",
                            "email",
                            "mail",
                            user.email,
                        ),
                        # Phone
                        form_field(
                            "Telefono",
                            "Telefono del cliente",
                            "tel",
                            "phone",
                            "phone",
                            user.phone,
                        ),
                        # Address
                        form_field(
                            "Dirección",
                            "",
                            "text",
                            "address",
                            "home",
                            user.address,
                        ),
                        # Payments
                        form_field(
                            "Pago ($)",
                            "Pago del cliente",
                            "number",
                            "payments",
                            "dollar-sign",
                            user.payments.to(str),
                        ),
                        # Status
                        rx.vstack(
                            rx.hstack(
                                rx.icon("truck", size=16, stroke_width=1.5),
                                rx.text("Status"),
                                align="center",
                                spacing="2",
                            ),
                            rx.radio(
                                ["Entregado", "Pendiente", "Cancelado"],
                                default_value=user.status,
                                name="status",
                                direction="row",
                                as_child=True,
                                required=True,
                            ),
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancelar",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Actualizar Cliente"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.update_customer_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def _header_cell(text: str, icon: str):
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def main_table():
    return rx.fragment(
        rx.flex(
            add_customer_button(),
            rx.spacer(),
            rx.cond(
                State.sort_reverse,
                rx.icon(
                    "arrow-down-z-a",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
                rx.icon(
                    "arrow-down-a-z",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
            ),
            rx.select(
                ["name", "email", "phone", "address", "payments", "date", "status"],
                placeholder="Sort By: Name",
                size="3",
                on_change=lambda sort_value: State.sort_values(sort_value),
            ),
            rx.input(
                rx.input.slot(rx.icon("search")),
                placeholder="Search here...",
                size="3",
                max_width="225px",
                width="100%",
                variant="surface",
                on_change=lambda value: State.filter_values(value),
            ),
            justify="end",
            align="center",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Nombre", "user"),
                    _header_cell("Correo", "mail"),
                    _header_cell("Teléfono", "phone"),
                    _header_cell("Dirección", "home"),
                    _header_cell("Pagos", "dollar-sign"),
                    _header_cell("Fecha", "calendar"),
                    _header_cell("Estado", "truck"),
                    _header_cell("Acciones", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(State.users, show_customer)),
            variant="surface",
            size="3",
            width="100%",
            on_mount=State.load_entries,
        ),
    )
