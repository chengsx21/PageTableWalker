FILE_NAME = "memory.txt"

HEX = 16
VPN0_BIT = 5
VPN1_BIT = 5
PPN_BIT = 5
PDE_BIT = 7
PTE_BIT = 7
OFFSET_BIT = 5
PAGE_DIR_BASE_ADDR = 0x220

MEMORY = []

VA_LIST = [
    "6c74",
    "6b22",
    "03df",
    "69dc",
    "317a",
    "4546",
    "2c03",
    "7fd7",
    "390e",
    "748b",
]


def init_memory():
    global MEMORY
    with open(FILE_NAME, "r") as f:
        lines = f.readlines()
        for line in lines:
            MEMORY += [int(data, HEX) for data in line.split(":")[1].split(" ") if data.strip()]


def parse_virtual_address(va):
    va = int(va, HEX)
    pde_index = (va >> (VPN1_BIT + OFFSET_BIT)) & ((0x1 << VPN0_BIT) - 1)
    pde_content = MEMORY[PAGE_DIR_BASE_ADDR + pde_index]
    pde_valid = (pde_content >> PDE_BIT) & 0x1
    pt = pde_content & ((0x1 << PDE_BIT) - 1)
    print(f"Virtual Address {va:04x}")
    print(f"  --> pde index: 0x{pde_index:02x}  pde contents: (valid {pde_valid}, pt 0x{pt:02x})")
    if (pde_valid):
        pte_index = (va >> OFFSET_BIT) & ((0x1 << VPN1_BIT) - 1)
        pte_content = MEMORY[(pt << OFFSET_BIT) + pte_index]
        pte_valid = (pte_content >> PTE_BIT) & 0x1
        pfn = pte_content & ((0x1 << PDE_BIT) - 1)
        print(f"    --> pte index: 0x{pte_index:02x}  pde contents: (valid {pte_valid}, pfn 0x{pfn:02x})")
        if (pte_valid):
            offset = va & ((0x1 << OFFSET_BIT) - 1)
            pa = (pfn << OFFSET_BIT) + offset
            pa_value = MEMORY[pa]
            print(f"      --> Translates to Physical Address 0x{pa:03x} --> Value: {pa_value:02x}")
        else:
            print("      --> Fault (page table entry not valid)")
    else:
        print("      --> Fault (page directory entry not valid)")


if __name__ == "__main__":    
    init_memory()
    for va in VA_LIST:
        parse_virtual_address(va)
