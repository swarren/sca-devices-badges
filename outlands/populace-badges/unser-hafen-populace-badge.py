#!/usr/bin/env python3

import os
import subprocess
import svgwrite

british_racing_green = '#004225'
forest_green = '#228b22'
primary_green = 'green'
green = forest_green

harvest_gold = '#da9100'
alt_yellow = '#dada00'
alt_yellow2= '#e0d000'
primary_yellow = 'yellow'
yellow = alt_yellow2

phys_size = 8 # inches
user_size = 8000

def abs_rel_path(d, parent, coords, **kwargs):
    p = d.path(d='M %d %d' % coords[0], **kwargs)
    p.push('l', coords[1:])
    p.push('Z')
    parent.add(p)

def rect_at(d, parent, x, y, w, h, **kwargs):
    coords = [
        (x, y),
        (w, 0),
        (0, h),
        (-w, 0),
        (0, -h)]
    abs_rel_path(d, parent, coords, **kwargs)

def gen_unser_hafen(d, parent, outer_cap_fn_name, inner_cap_fn_name):
    half_user_size = user_size / 2
    outline_width = 40 # ~1mm
    cross_width = 20 # ~0.5mm
    bordure_width = 600 # 0.6in
    gate_bar_size = 600 # 0.6in
    gate_bar_gap = 600 # 0.5in
    gate_arrow_height = 500 # 0.5in
    gate_h_bar_count = 4 # Can be even or odd
    gate_v_bar_count = 5 # Must be odd
    bad_stroke_width = 500

    def cap_flat(path, xdir, width, middle_bar):
        if middle_bar:
            width /= 2
        p.push('l', (xdir * width, 0))

    def cap_round(path, xdir, width, middle_bar):
        if middle_bar:
            p.push('c',
                (0, width / 3),
                (xdir * width / 2, width / 3),
                (xdir * width / 2, width / 3))
        else:
            p.push('c',
                (0, width / 3),
                (xdir * width, width / 3),
                (xdir * width, 0))

    def cap_rect(path, xdir, width, middle_bar):
        if middle_bar:
            width /= 2
        p.push('l',
            (0, gate_arrow_height),
            (xdir * width, 0),
            (0, -gate_arrow_height))

    def cap_half_flanged_arrow(path, xdir, width, middle_bar):
        if middle_bar:
            raise Exception("half cap function used on middle bar!")
        p.push('l',
            (0, gate_arrow_height),
            (xdir * (width + (gate_bar_gap / 2)), -gate_arrow_height),
            (xdir * -(gate_bar_gap / 2), 0))

    def cap_full_flanged_arrow(path, xdir, width, middle_bar):
        p.push('l',
            (xdir * -(gate_bar_gap / 2), 0),
            (xdir * (width + gate_bar_gap) / 2, gate_arrow_height))
        if not middle_bar:
            p.push('l',
                (xdir * (width + gate_bar_gap) / 2, -gate_arrow_height),
                (xdir * -(gate_bar_gap / 2), 0))

    def cap_half_flanged_arrow_curved(path, xdir, width, middle_bar):
        if middle_bar:
            raise Exception("half cap function used on middle bar!")
        w = (width + (gate_bar_gap / 2))
        p.push('l',
            (0, gate_arrow_height),
            'c',
            (xdir * w * 0.35, -gate_arrow_height * 0.5),
            (xdir * w * 0.35, -gate_arrow_height * 0.5),
            (xdir * w, -gate_arrow_height),
            'l',
            (xdir * -(gate_bar_gap / 2), 0))

    def cap_full_flanged_arrow_curved(path, xdir, width, middle_bar):
        w = (width + gate_bar_gap) / 2
        p.push('l',
            (xdir * -(gate_bar_gap / 2), 0),
            'c',
            (xdir * w * 0.65, gate_arrow_height * 0.5),
            (xdir * w * 0.65, gate_arrow_height * 0.5),
            (xdir * w, gate_arrow_height))
        if not middle_bar:
            p.push('c',
                (xdir * w * 0.35, -gate_arrow_height * 0.5),
                (xdir * w * 0.35, -gate_arrow_height * 0.5),
                (xdir * w, -gate_arrow_height),
                'l',
                (xdir * -(gate_bar_gap / 2), 0))

    def cap_half_narrow_flanged_arrow(path, xdir, width, middle_bar):
        if middle_bar:
            raise Exception("half cap function used on middle bar!")
        p.push('l',
            (0, gate_arrow_height),
            (xdir * (width + (gate_bar_gap / 4)), -gate_arrow_height),
            (xdir * -(gate_bar_gap / 4), 0))

    def cap_full_narrow_flanged_arrow(path, xdir, width, middle_bar):
        p.push('l',
            (xdir * -(gate_bar_gap / 4), 0),
            (xdir * ((width / 2) + (gate_bar_gap / 4)), gate_arrow_height))
        if not middle_bar:
            p.push('l',
                (xdir * ((width / 2) + (gate_bar_gap / 4)), -gate_arrow_height),
                (xdir * -(gate_bar_gap / 4), 0))

    def cap_half_narrow_flanged_arrow_curved(path, xdir, width, middle_bar):
        if middle_bar:
            raise Exception("half cap function used on middle bar!")
        w = width + (gate_bar_gap / 4)
        p.push('l',
            (0, gate_arrow_height),
            'c',
            (xdir * w * 0.35, -gate_arrow_height * 0.5),
            (xdir * w * 0.35, -gate_arrow_height * 0.5),
            (xdir * w, -gate_arrow_height),
            'l',
            (xdir * -(gate_bar_gap / 4), 0))

    def cap_full_narrow_flanged_arrow_curved(path, xdir, width, middle_bar):
        w = (width / 2) + (gate_bar_gap / 4)
        p.push('l',
            (xdir * -(gate_bar_gap / 4), 0),
            'c',
            (xdir * w * 0.65, gate_arrow_height * 0.5),
            (xdir * w * 0.65, gate_arrow_height * 0.5),
            (xdir * w, gate_arrow_height))
        if not middle_bar:
            p.push('c',
                (xdir * w * 0.35, -gate_arrow_height * 0.5),
                (xdir * w * 0.35, -gate_arrow_height * 0.5),
                (xdir * w, -gate_arrow_height),
                'l',
                (xdir * -(gate_bar_gap / 4), 0))

    def cap_half_inner_arrow(path, xdir, width, middle_bar):
        if middle_bar:
            raise Exception("half cap function used on middle bar!")
        p.push('l',
            (0, gate_arrow_height),
            (xdir * width, -gate_arrow_height))

    def cap_full_inner_arrow(path, xdir, width, middle_bar):
        p.push('l', (xdir * width / 2, gate_arrow_height))
        if not middle_bar:
            p.push('l', (xdir * width / 2, -gate_arrow_height))

    def cap_half_inner_arrow_curved(path, xdir, width, middle_bar):
        if middle_bar:
            raise Exception("half cap function used on middle bar!")
        p.push('l',
            (0, gate_arrow_height),
            'c',
            (xdir * width * 0.35, -gate_arrow_height * 0.5),
            (xdir * width * 0.35, -gate_arrow_height * 0.5),
            (xdir * width, -gate_arrow_height))

    def cap_full_inner_arrow_curved(path, xdir, width, middle_bar):
        w = width / 2
        h = gate_arrow_height
        p.push('c',
            (xdir * w * 0.65, h * 0.5),
            (xdir * w * 0.65, h * 0.5),
            (xdir * w, h))
        if not middle_bar:
            p.push('c',
                (xdir * w * 0.35, -h * 0.5),
                (xdir * w * 0.35, -h * 0.5),
                (xdir * w, -h))

    ocapfn = locals()['cap_' + outer_cap_fn_name]
    icapfn = locals()['cap_' + inner_cap_fn_name]

    # FIXME: Get this from function attributes somehow
    if ocapfn == cap_flat and icapfn == cap_flat:
        gate_arrow_height = 0

    # Overall group
    g = d.g()
    parent.add(g)

    # Bordure (behind field)
    rect_at(d, g,
        0, 0,
        half_user_size, user_size,
        stroke_width=outline_width, stroke='black', fill=yellow)
    rect_at(d, g,
        half_user_size, 0,
        half_user_size, user_size,
        stroke_width=outline_width, stroke='black', fill=green)

    # Field (inside bordure, behind gate)
    rect_at(d, g,
        bordure_width, bordure_width,
        half_user_size - bordure_width, user_size - (2 * bordure_width),
        stroke_width=outline_width, stroke='black', fill=green)
    rect_at(d, g,
        half_user_size, bordure_width,
        half_user_size - bordure_width, user_size - (2 * bordure_width),
        stroke_width=outline_width, stroke='black', fill=yellow)

    # Gate
    mid_gate_v_bar_count_per_side = (gate_v_bar_count - 3) / 2
    h_gaps_per_side = int((gate_v_bar_count - 1) / 2)
    v_gaps = gate_h_bar_count
    h_gaps = gate_v_bar_count - 1
    gate_side_w = (
        (gate_bar_size / 2) + # inner half width v bar
        (gate_bar_size * mid_gate_v_bar_count_per_side) + # middle v bar per side
        gate_bar_size + # outer half width v bar
        (gate_bar_gap * h_gaps_per_side)
    )
    gate_h = (
        gate_bar_size +
        (gate_bar_size * (gate_h_bar_count - 1)) +
        (gate_bar_gap * v_gaps) +
        gate_arrow_height
    )
    gate_side_h = gate_h - gate_arrow_height
    gate_y_pos = bordure_width + ((user_size - (gate_h + (2 * bordure_width))) / 2)

    for xdir, gate_color, gap_color in ((1, yellow, green), (-1, green, yellow)):
        # Gate outline
        start = (half_user_size, gate_y_pos)
        p = d.path(d='M %d %d' % start, stroke_width=outline_width, stroke='black', fill=gate_color)
        p.push('l',
            (xdir * -gate_side_w, 0), # top
            (0, gate_side_h), # outer side
        )
        for i in range(h_gaps_per_side):
            if i == 0:
                fn = ocapfn
            else:
                fn = icapfn
            fn(p, xdir, gate_bar_size, False)

            p.push('l',
                (0, -gate_bar_gap), # left side of gap
                (xdir * gate_bar_gap, 0), # top side of gap
                (0, gate_bar_gap), # right side of gap
            )
        icapfn(p, xdir, gate_bar_size, True)
        p.push('l', (0, -gate_side_h)) # inner side
        p.push('Z')
        g.add(p)
        # Inner gaps
        base_gap_x_pos = half_user_size
        base_gap_x_pos -= xdir * int(gate_bar_size / 2)
        base_gap_x_pos -= xdir * gate_bar_gap
        for yi in range(v_gaps - 1):
            for xi in range(h_gaps_per_side):
                start = (
                    base_gap_x_pos - (xdir * xi * (gate_bar_size + gate_bar_gap)),
                    gate_y_pos + gate_bar_size + (yi * (gate_bar_size + gate_bar_gap)))
                p.push('M', start)
                p.push('l', [
                    (xdir * gate_bar_gap, 0),
                    (0, gate_bar_gap),
                    (xdir * -gate_bar_gap, 0),
                    (0, -gate_bar_gap)])
                p.push('Z')
    # Detail crosses
    for yi in range(v_gaps):
        for xi in range(h_gaps):
            top_left = (
                half_user_size - gate_side_w + gate_bar_size + (xi * (gate_bar_size + gate_bar_gap)),
                gate_y_pos + gate_bar_size + (yi * (gate_bar_size + gate_bar_gap)))
            if xi == 0 and yi == 0:
                cross_len = gate_bar_size
            elif xi == 0 or yi == 0:
                cross_len = gate_bar_size / 2
            else:
                cross_len = gate_bar_size
            p = d.path(d='M %d %d' % top_left, stroke_width=cross_width, stroke='black')
            p.push('l', (-cross_len, -cross_len))
            g.add(p)

            if xi == h_gaps - 1 and yi != v_gaps - 1:
                bot_right = (top_left[0] + gate_bar_gap, top_left[1] + gate_bar_gap)
                cross_len = gate_bar_size / 2
                p = d.path(d='M %d %d' % bot_right, stroke_width=cross_width, stroke='black')
                p.push('l', (cross_len, cross_len))
                g.add(p)

            top_right = (top_left[0] + gate_bar_gap, top_left[1])
            if xi == (h_gaps - 1) and yi == 0:
                cross_len = gate_bar_size
            elif xi == (h_gaps - 1) or yi == 0:
                cross_len = gate_bar_size / 2
            else:
                cross_len = gate_bar_size
            p = d.path(d='M %d %d' % top_right, stroke_width=cross_width, stroke='black')
            p.push('l', (cross_len, -cross_len))
            g.add(p)

            if xi == 0 and yi != v_gaps - 1:
                bot_left = (top_left[0], top_left[1] + gate_bar_gap)
                cross_len = gate_bar_size / 2
                p = d.path(d='M %d %d' % bot_left, stroke_width=cross_width, stroke='black')
                p.push('l', (-cross_len, cross_len))
                g.add(p)

def gen_one(filename, outer_cap_fn_name, inner_cap_fn_name):
    d = svgwrite.Drawing(filename, profile='full', size=('%fin' % phys_size, '%fin' % phys_size))
    d.viewbox(0, 0, user_size, user_size)
    gen_unser_hafen(d, d, outer_cap_fn_name, inner_cap_fn_name)
    d.save()

cap_configs = (
    ('half_flanged_arrow', 'full_flanged_arrow'),
    ('half_flanged_arrow_curved', 'full_flanged_arrow_curved'),
    ('full_flanged_arrow', 'full_flanged_arrow'),
    ('full_flanged_arrow_curved', 'full_flanged_arrow_curved'),
    ('half_narrow_flanged_arrow', 'full_narrow_flanged_arrow'),
    ('half_narrow_flanged_arrow_curved', 'full_narrow_flanged_arrow_curved'),
    ('full_narrow_flanged_arrow', 'full_narrow_flanged_arrow'),
    ('full_narrow_flanged_arrow_curved', 'full_narrow_flanged_arrow_curved'),
    ('half_inner_arrow', 'full_inner_arrow'),
    ('half_inner_arrow_curved', 'full_inner_arrow_curved'),
    ('full_inner_arrow', 'full_inner_arrow'),
    ('full_inner_arrow_curved', 'full_inner_arrow_curved'),
)

def gen_many(img_dir):
    fn_base = img_dir + '/unser-hafen-populace-badge-%d.generated.%s'
    img_id = 0
    for (ocap, icap) in cap_configs:
        svg_fn = fn_base % (img_id, 'svg')
        pdf_fn = fn_base % (img_id, 'pdf')
        gen_one(svg_fn, ocap, icap)
        subprocess.call(['inkscape', svg_fn, '--export-pdf', pdf_fn])
        img_id += 1

def gen_n_up(img_dir):
    fn_base = img_dir + '/unser-hafen-populace-badge-all.generated.'
    svg_fn = fn_base + 'svg'
    pdf_fn = fn_base + 'pdf'

    count = len(cap_configs)
    xcount = 4
    ycount = count / xcount
    phys_gap = 2 # inches
    user_gap = user_size * (phys_gap / phys_size)
    x_user_size = (xcount * user_size) + ((xcount - 1) * user_gap)
    y_user_size = (ycount * user_size) + ((ycount - 1) * user_gap)
    x_phys_size = (xcount * phys_size) + ((xcount - 1) * phys_gap)
    y_phys_size = (ycount * phys_size) + ((ycount - 1) * phys_gap)

    d = svgwrite.Drawing(svg_fn, profile='full', size=('%fin' % x_phys_size, '%din' % y_phys_size))
    d.viewbox(0, 0, x_user_size, y_user_size)
    x = 0
    y = 0
    for (ocap, icap) in cap_configs:
        xo = x * (user_size + user_gap)
        yo = y * (user_size + user_gap)
        g = svgwrite.container.Group(transform='translate(%d,%d)' % (xo, yo))
        d.add(g)
        gen_unser_hafen(d, g, ocap, icap)
        x += 1
        if x >= xcount:
            x = 0
            y += 1
    d.save()
    subprocess.call(['inkscape', svg_fn, '--export-pdf', pdf_fn])

img_dir = 'unser-hafen-populace-badge'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)
gen_many(img_dir)
gen_n_up(img_dir)
