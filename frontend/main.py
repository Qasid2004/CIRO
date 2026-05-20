import flet as ft
import asyncio
import re
import random

# =========================================================
# SAFE FLET COMPATIBILITY LAYER
# =========================================================

class _PaddingCompat:
    @staticmethod
    def only(left=0, top=0, right=0, bottom=0):
        return ft.Padding(left, top, right, bottom)

    @staticmethod
    def all(value=0):
        return ft.Padding(value, value, value, value)


class _MarginCompat:
    @staticmethod
    def only(left=0, top=0, right=0, bottom=0):
        return ft.Margin(left, top, right, bottom)

    @staticmethod
    def all(value=0):
        return ft.Margin(value, value, value, value)


class _BorderCompat:
    @staticmethod
    def all(width=1, color="#000"):
        return ft.Border(
            left=ft.BorderSide(width, color),
            top=ft.BorderSide(width, color),
            right=ft.BorderSide(width, color),
            bottom=ft.BorderSide(width, color),
        )

    @staticmethod
    def only(left=None, top=None, right=None, bottom=None):
        return ft.Border(
            left=left,
            top=top,
            right=right,
            bottom=bottom,
        )


class _AlignmentCompat:
    center = ft.Alignment(0, 0)


ft.padding = _PaddingCompat
ft.margin = _MarginCompat
ft.border = _BorderCompat
ft.alignment = _AlignmentCompat

# =========================================================
# COLORS
# =========================================================

C_BG = "#ffffff"
C_SURFACE = "#f8fafc"
C_BORDER = "#e2e8f0"

C_BLUE = "#1a7fc4"
C_BLUE_LIGHT = "#e8f4fc"

C_TEXT = "#0f172a"
C_MUTED = "#64748b"

C_RED = "#dc2626"
C_RED_LIGHT = "#fee2e2"

C_GREEN = "#16a34a"
C_GREEN_LIGHT = "#dcfce7"

C_AMBER = "#d97706"
C_AMBER_LIGHT = "#fef3c7"

# =========================================================
# HELPERS
# =========================================================

P = ft.Padding
M = ft.Margin


def badge(text, bg, fg):
    return ft.Container(
        content=ft.Text(
            text,
            size=10,
            weight=ft.FontWeight.BOLD,
            color=fg,
        ),
        bgcolor=bg,
        border_radius=20,
        padding=P(10, 4, 10, 4),
    )


def divider():
    return ft.Container(height=1, bgcolor=C_BORDER)


def extract_location(text):
    match = re.search(r"[A-Z]-\d+", text.upper())
    if match:
        return match.group(0)
    return "Unknown"


def detect_crisis(text):
    txt = text.lower()
    location = extract_location(text)

    # FLOOD
    if any(x in txt for x in ["flood", "pani", "baarish", "water"]):
        return {
            "type": "Urban Flooding",
            "severity": "Critical",
            "location": location,
            "confidence": "96%",
            "before": random.randint(70, 95),
            "after": random.randint(20, 40),
            "weather": {
                "alert": "HEAVY RAIN",
                "rainfall": f"{random.randint(30,60)} mm/hr",
                "risk": "HIGH",
            },
            "traffic": {
                "status": "BLOCKED",
                "speed": "0 km/h",
            },
            "logs": [
                f"Social media flood signals detected from {location}",
                f"Rainfall spike confirmed near {location}",
                "Emergency pumps recommended",
                "Ambulance rerouting activated",
            ],
        }

    # ELECTRIC
    if any(x in txt for x in ["wire", "electric", "khamba", "bijli"]):
        return {
            "type": "Electrical Hazard",
            "severity": "Critical",
            "location": location,
            "confidence": "92%",
            "before": random.randint(60, 90),
            "after": random.randint(10, 30),
            "weather": {
                "alert": "STORM CONDITIONS",
                "rainfall": f"{random.randint(10,25)} mm/hr",
                "risk": "MEDIUM",
            },
            "traffic": {
                "status": "DIVERTED",
                "speed": "12 km/h",
            },
            "logs": [
                f"Live electrical wires detected in {location}",
                "Traffic police alerted",
                "Grid shutdown initiated",
                "Danger perimeter established",
            ],
        }

    # FIRE
    if any(x in txt for x in ["fire", "smoke", "aag"]):
        return {
            "type": "Fire Emergency",
            "severity": "High",
            "location": location,
            "confidence": "89%",
            "before": random.randint(50, 80),
            "after": random.randint(10, 20),
            "weather": {
                "alert": "HIGH TEMPERATURE",
                "rainfall": "0 mm/hr",
                "risk": "LOW",
            },
            "traffic": {
                "status": "SLOW",
                "speed": "20 km/h",
            },
            "logs": [
                "Smoke density increasing",
                "Fire brigade dispatched",
                "Nearby roads sealed",
                "Evacuation alerts sent",
            ],
        }

    return {
        "type": "Unknown Situation",
        "severity": "Medium",
        "location": location,
        "confidence": "70%",
        "before": 50,
        "after": 35,
        "weather": {
            "alert": "NORMAL",
            "rainfall": "0 mm/hr",
            "risk": "LOW",
        },
        "traffic": {
            "status": "CLEAR",
            "speed": "40 km/h",
        },
        "logs": [
            "Signals collected",
            "Situation under observation",
        ],
    }


# =========================================================
# MAIN
# =========================================================

def main(page: ft.Page):

    page.title = "CIRO"
    page.bgcolor = C_SURFACE
    page.padding = 0
    page.window_width = 1400
    page.window_height = 900

    # =====================================================
    # HEADER
    # =====================================================

    header = ft.Container(
        content=ft.Row(
            [
                # GOOGLE FOR DEVELOPERS
                ft.Image(
                    src="assets/googlefordevelopers.png",
                    width=250,
                    height=125,
                ),

                # CENTER TITLE
                ft.Column(
                    [
                        ft.Text(
                            "CIRO",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=C_BLUE,
                            text_align=ft.TextAlign.CENTER,
                        ),

                        ft.Text(
                            "Crisis Intelligence & Response Orchestrator",
                            size=12,
                            color=C_MUTED,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),

                # COLLABORATION LOGOS
                ft.Row(
                    [
                        ft.Text(
                            "In collaboration with",
                            size=11,
                            color=C_MUTED,
                            weight=ft.FontWeight.W_600,
                        ),

                        ft.Image(
                            src="assets/techdestinationpakistan_logo.png",
                            width=100,
                            height=50,
                        ),

                        ft.Image(
                            src="assets/telenor4g.png",
                            width=100,
                            height=50,
                        ),

                        ft.Image(
                            src="assets/innovista.png",
                            width=100,
                            height=50,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],

            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),

        bgcolor=C_BG,

        padding=P(24, 18, 24, 18),

        border=ft.border.only(
            bottom=ft.BorderSide(1, C_BORDER)
        ),
    )


    # =====================================================
    # INTRO SPLASH
    # =====================================================

    intro_text = ft.Text(
        "CIRO",
        size=90,
        weight=ft.FontWeight.BOLD,
        color=C_BLUE,
        opacity=0,
        animate_opacity=800,
    )

    intro_overlay = ft.Container(
        content=ft.Column(
            [
                intro_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    ),

    alignment=ft.alignment.center,

    bgcolor=C_BG,

    expand=True,

    opacity=1,

    animate_opacity=600,
)

    # =====================================================
    # INPUT
    # =====================================================

    social_input = ft.TextField(
        hint_text="Example: G-10 mein flood aa gaya hai aur roads band hain",
        multiline=True,
        min_lines=4,
        max_lines=6,
        border_color=C_BORDER,
        focused_border_color=C_BLUE,
        border_radius=12,
        bgcolor=C_BG,
)

    # =====================================================
    # AGENT PIPELINE
    # =====================================================

    agents_column = ft.Column(spacing=10)

    agent_names = [
        "Signal Collector",
        "Crisis Detector",
        "Priority Ranker",
        "Action Planner",
        "Executor",
    ]

    agent_controls = []

    for name in agent_names:

        status = ft.Text(
            "Waiting",
            size=11,
            color=C_MUTED,
            weight=ft.FontWeight.BOLD,
        )

        row = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        width=12,
                        height=12,
                        border_radius=20,
                        bgcolor="#cbd5e1",
                    ),
                    ft.Text(
                        name,
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                    ),
                    status,
                ]
            ),
            bgcolor=C_BG,
            padding=14,
            border_radius=12,
            border=ft.border.all(1, C_BORDER),
        )

        agents_column.controls.append(row)
        agent_controls.append((row, status))

    # =====================================================
    # BEFORE AFTER
    # =====================================================

    before_bar = ft.ProgressBar(
        width=500,
        value=0,
        color=C_RED,
        bgcolor="#fecaca",
    )

    after_bar = ft.ProgressBar(
        width=500,
        value=0,
        color=C_GREEN,
        bgcolor="#bbf7d0",
    )

    before_text = ft.Text("0%", weight=ft.FontWeight.BOLD)
    after_text = ft.Text("0%", weight=ft.FontWeight.BOLD)

    before_after_card = ft.Container(
        visible=False,
        bgcolor=C_BG,
        border_radius=14,
        border=ft.border.all(1, C_BORDER),
        padding=20,
        content=ft.Column(
            [
                ft.Text(
                    "Before vs After Response",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Container(height=10),

                ft.Row([
                    ft.Text("Before", width=70),
                    before_bar,
                    before_text,
                ]),

                ft.Container(height=10),

                ft.Row([
                    ft.Text("After", width=70),
                    after_bar,
                    after_text,
                ]),
            ]
        ),
    )

    # =====================================================
    # CRISIS CARD
    # =====================================================

    crisis_content = ft.Column()

    crisis_card = ft.Container(
        visible=False,
        bgcolor=C_BG,
        border_radius=14,
        border=ft.border.all(1, C_BORDER),
        padding=20,
        content=crisis_content,
    )

    # =====================================================
    # LOGS
    # =====================================================

    logs_column = ft.Column(
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
        height=220,
    )

    logs_card = ft.Container(
        visible=False,
        bgcolor=C_BG,
        border_radius=14,
        border=ft.border.all(1, C_BORDER),
        padding=20,
        content=ft.Column([
            ft.Text(
                "Agent Logs",
                size=16,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Container(height=10),
            logs_column,
        ]),
    )

    # =====================================================
    # WEATHER
    # =====================================================

    weather_column = ft.Column(
    [
        ft.Text(
            "Weather Intelligence",
            size=16,
            weight=ft.FontWeight.BOLD,
        ),

        ft.Container(height=12),

        ft.Row([
            ft.Text("Alert", expand=True),
            badge("HEAVY RAIN", C_RED_LIGHT, C_RED)
        ]),

        divider(),

        ft.Row([
            ft.Text("Rainfall", expand=True),
            ft.Text("42 mm/hr")
        ]),

        divider(),

        ft.Row([
            ft.Text("Flood Risk", expand=True),
            badge("HIGH", C_AMBER_LIGHT, C_AMBER)
        ]),
    ]
)

    weather_card = ft.Container(
        bgcolor=C_BG,
        border_radius=14,
        border=ft.border.all(1, C_BORDER),
        padding=20,
        content=weather_column,
    )

    # =====================================================
    # TRAFFIC
    # =====================================================

    traffic_column = ft.Columntraffic_column = ft.Column(
    [
        ft.Text(
            "Traffic Intelligence",
            size=16,
            weight=ft.FontWeight.BOLD,
        ),

        ft.Container(height=12),

        ft.Row([
            ft.Text("Road Status", expand=True),
            badge("BLOCKED", C_RED_LIGHT, C_RED)
        ]),

        divider(),

        ft.Row([
            ft.Text("Average Speed", expand=True),
            ft.Text("12 km/h")
        ]),
    ]
)

    traffic_card = ft.Container(
        bgcolor=C_BG,
        border_radius=14,
        border=ft.border.all(1, C_BORDER),
        padding=20,
        content=traffic_column,
    )

    # =====================================================
    # ANALYZE
    # =====================================================

    async def run_pipeline(e):

        text = social_input.value

        if not text:
            return

        result = detect_crisis(text)

        # RESET
        logs_column.controls.clear()

        before_bar.value = 0
        after_bar.value = 0

        before_after_card.visible = False
        crisis_card.visible = False
        logs_card.visible = False

        page.update()

        # PIPELINE
        for i, (row, status) in enumerate(agent_controls):

            status.value = "Processing"
            status.color = C_BLUE

            row.bgcolor = "#eff6ff"

            page.update()

            await asyncio.sleep(1)

            status.value = "Done"
            status.color = C_GREEN

            row.bgcolor = "#f0fdf4"

            page.update()

        # =================================================
        # WEATHER UPDATE
        # =================================================

        weather = result["weather"]

        weather_column.controls.clear()

        weather_column.controls.extend([
            ft.Text(
                "Weather Intelligence",
                size=16,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Container(height=12),

            ft.Row([
                ft.Text("Alert", expand=True),
                badge(weather["alert"], C_RED_LIGHT, C_RED)
            ]),

            divider(),

            ft.Row([
                ft.Text("Rainfall", expand=True),
                ft.Text(weather["rainfall"])
            ]),

            divider(),

            ft.Row([
                ft.Text("Flood Risk", expand=True),
                badge(weather["risk"], C_AMBER_LIGHT, C_AMBER)
            ]),
        ])

        # =================================================
        # TRAFFIC UPDATE
        # =================================================

        traffic = result["traffic"]

        traffic_column.controls.clear()

        traffic_column.controls.extend([
            ft.Text(
                "Traffic Intelligence",
                size=16,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Container(height=12),

            ft.Row([
                ft.Text("Road Status", expand=True),
                badge(traffic["status"], C_RED_LIGHT, C_RED)
            ]),

            divider(),

            ft.Row([
                ft.Text("Average Speed", expand=True),
                ft.Text(traffic["speed"])
            ]),
        ])

        # =================================================
        # BEFORE AFTER
        # =================================================

        before_after_card.visible = True

        before = result["before"]
        after = result["after"]

        before_text.value = f"{before}%"
        after_text.value = f"{after}%"

        before_bar.value = before / 100
        after_bar.value = after / 100

        # =================================================
        # CRISIS CARD
        # =================================================

        crisis_content.controls.clear()

        crisis_content.controls.extend([
            ft.Text(
                "Crisis Detected",
                size=16,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Container(height=10),

            ft.Row([
                ft.Text("Type", expand=True),
                ft.Text(result["type"])
            ]),

            divider(),

            ft.Row([
                ft.Text("Location", expand=True),
                ft.Text(result["location"])
            ]),

            divider(),

            ft.Row([
                ft.Text("Severity", expand=True),
                badge(result["severity"], C_RED_LIGHT, C_RED)
            ]),

            divider(),

            ft.Row([
                ft.Text("Confidence", expand=True),
                ft.Text(result["confidence"])
            ]),
        ])

        crisis_card.visible = True

        # =================================================
        # LOGS
        # =================================================

        logs_card.visible = True

        for log in result["logs"]:

            logs_column.controls.append(
                ft.Container(
                    content=ft.Text(log, size=12),
                    bgcolor="#f8fafc",
                    border_radius=10,
                    padding=12,
                    border=ft.border.only(
                        left=ft.BorderSide(3, C_BLUE)
                    ),
                )
            )

            page.update()
            await asyncio.sleep(0.7)

        page.update()

    # =====================================================
    # BUTTON
    # =====================================================

    analyze_btn = ft.ElevatedButton(
        "Analyze Crisis",
        on_click=run_pipeline,
        style=ft.ButtonStyle(
            bgcolor=C_BLUE,
            color="white",
            padding=P(30, 16, 30, 16),
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    # =====================================================
    # RIGHT PANEL
    # =====================================================

    right_panel = ft.Column(
        [
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Social Media Input",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),

                    ft.Container(height=12),

                    social_input,

                    ft.Container(height=16),

                    ft.Row([
                        analyze_btn
                    ]),
                ]),
                bgcolor=C_BG,
                border_radius=14,
                border=ft.border.all(1, C_BORDER),
                padding=20,
            ),

            ft.Container(height=14),

            weather_card,

            ft.Container(height=14),

            traffic_card,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # =====================================================
    # LEFT PANEL
    # =====================================================

    left_panel = ft.Column(
        [
            ft.Text(
                "AGENT PIPELINE",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=C_MUTED,
            ),

            ft.Container(height=14),

            agents_column,

            ft.Container(height=20),

            before_after_card,

            ft.Container(height=20),

            crisis_card,

            ft.Container(height=20),

            logs_card,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # =====================================================
    # BODY
    # =====================================================

    body = ft.Row(
        [
            ft.Container(
                content=left_panel,
                expand=2,
                padding=20,
            ),

            ft.VerticalDivider(width=1, color=C_BORDER),

            ft.Container(
                content=right_panel,
                expand=1,
                padding=20,
                bgcolor=C_SURFACE,
            ),
        ],
        expand=True,
    )

    # =====================================================
    # ROOT
    # =====================================================

    main_ui = ft.Column(
        [
            header,
            body,
        ],
        spacing=0,
        expand=True,
    )

    root = ft.Stack(
        [
            main_ui,
            intro_overlay,
        ],
        expand=True,
    )

    page.add(root)

    # =====================================================
# INTRO ANIMATION
# =====================================================

    async def start_intro():

        await asyncio.sleep(0.3)

        intro_text.opacity = 1
        page.update()

        await asyncio.sleep(1.8)

        intro_overlay.opacity = 0
        page.update()

        await asyncio.sleep(0.8)

        intro_overlay.visible = False
        page.update()

    page.run_task(start_intro)


# =========================================================
# RUN
# =========================================================

ft.app(target=main)