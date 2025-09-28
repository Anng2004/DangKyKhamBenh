#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def print_success(message: str, prefix: str = "✅") -> None:
    print(f"{prefix} {message}")

def print_error(message: str, prefix: str = "❌") -> None:
    print(f"{prefix} {message}")

def print_warning(message: str, prefix: str = "⚠️") -> None:
    print(f"{prefix} {message}")

def print_info(message: str, prefix: str = "ℹ️") -> None:
    print(f"{prefix} {message}")

def print_header(message: str, width: int = 50, char: str = "=") -> None:
    print("\n" + char * width)
    padding = (width - len(message)) // 2
    centered_message = " " * padding + message
    print(centered_message)
    print(char * width)

def print_separator(width: int = 50, char: str = "-") -> None:
    print(char * width)

def print_step(step_number: int, message: str, prefix: str = "🔄") -> None:
    print(f"{prefix} BƯỚC {step_number}: {message}")

def print_menu_item(number: int, description: str, icon: str = "") -> None:

    icon_part = f"{icon} " if icon else ""
    print(f"{number}. {icon_part}{description}")

def print_result_summary(title: str, items: list, prefix: str = "📊") -> None:

    print(f"\n{prefix} {title}:")
    for label, value in items:
        print(f"   • {label}: {value}")

def confirm_action(message: str, default: bool = False) -> bool:
    default_text = "(y/n)" if default else "(y/n)"
    response = input(f"❓ {message} {default_text}: ").strip().lower()
    
    if not response: 
        return default
    
    return response in ['y', 'yes', 'đồng ý', 'có']

def input_with_validation(prompt: str, validator=None, error_message: str = None) -> str:
    while True:
        value = input(f"➤ {prompt}: ").strip()
        
        if validator is None:
            return value
            
        if validator(value):
            return value
        else:
            error_msg = error_message or "Giá trị nhập vào không hợp lệ!"
            print_error(error_msg)

def print_table_header(headers: list, widths: list) -> None:
    header_line = ""
    separator_line = ""
    
    for i, (header, width) in enumerate(zip(headers, widths)):
        header_line += f"{header:<{width}} "
        separator_line += "-" * width + " "
    
    print(header_line.rstrip())
    print(separator_line.rstrip())

def print_table_row(values: list, widths: list) -> None:
    row_line = ""
    for value, width in zip(values, widths):
        row_line += f"{str(value):<{width}} "
    print(row_line.rstrip())

def success(message: str) -> None:
    print_success(message)

def error(message: str) -> None:
    print_error(message)

def warning(message: str) -> None:
    print_warning(message)

def info(message: str) -> None:
    print_info(message)