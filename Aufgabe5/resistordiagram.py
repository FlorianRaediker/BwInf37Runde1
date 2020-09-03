#!/usr/bin/env python3
import sys
import os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "site-packages/"))
from collections import Counter

import svgwrite
import svgwrite.shapes
import svgwrite.text
import svgwrite.container


class Resistor:
    def __init__(self, resistance):
        self.resistance = resistance
    
    def __repr__(self):
        return "Resistor(" + repr(self.resistance) + ")"
    
    def to_diagram(self):
        return str(self.resistance)
    
    def get_svg(self, resistor_size=(40, 10), wire_space=15, resistor_space=10, fill_color="rgb(218, 218, 218)",
                outline_color="black", text_color="black", font="Arial"):
        rect = svgwrite.shapes.Rect(size=resistor_size, fill=fill_color, stroke=outline_color)
        text = svgwrite.text.Text(str(self.resistance) + "Ω", (resistor_size[0] / 2, resistor_size[1] / 2),
                                  dy=["0.35em"], font_size="10", font_family=font,
                                  text_anchor="middle", fill=text_color)
        group = svgwrite.container.Group()
        group.add(rect)
        group.add(text)
        return group, resistor_size
    
    def save(self, filename, add_resistance=True, resistor_size=(40, 10), wire_space=15, resistor_space=10, fill_color="rgb(218, 218, 218)",
             outline_color="black", text_color="black", font="Arial", heading_size="20"):
        group, size = self.get_svg(resistor_size, wire_space, resistor_space, fill_color, outline_color, text_color,
                                   font)
        if add_resistance:
            group.translate(0, 20)
            text = svgwrite.text.Text("~{:.3f}Ω".format(self.resistance), (0, 15),
                                      font_size=heading_size, font_family=font,
                                      text_anchor="start", fill=text_color)
            draw = svgwrite.Drawing(size=(max(size[0], 100), size[1] + 20))
            draw.add(text)
        else:
            draw = svgwrite.Drawing(size=size)
        draw.add(group)
        draw.saveas(filename, True)


class ParallelResistor(Resistor):
    def __init__(self, r1, r2, *resistors):
        self._resistors = list((Resistor(i) if type(i) not in (ParallelResistor, SerialResistor, Resistor) else i
                                for i in [r1, r2, *resistors]))
        super().__init__(self._recalc_resistance())

    def _recalc_resistance(self):
        return 1 / (sum(1 / r.resistance for r in self.resistors))
    
    def __repr__(self):
        return "ParallelResistor(" + ",".join((repr(r) for r in self.resistors)) + ")"
    
    def to_diagram(self):
        return "P(" + " | ".join(r.to_diagram() for r in self.resistors) + ")"
    
    def get_svg(self, resistor_size=(40, 10), wire_space=15, resistor_space=10, fill_color="rgb(218, 218, 218)",
                outline_color="black", text_color="black", font="Arial"):
        group = svgwrite.container.Group()
        if len(self.resistors) == 0:
            return group
        resistor_svgs = [r.get_svg(resistor_size, wire_space, resistor_space, fill_color, outline_color, text_color,
                                   font) for r in self._resistors]
        max_width = max(resistor_svgs, key=lambda x: x[1][0])[1][0]
        half_wire_space = wire_space / 2
        x_parallel_end = 1.5 * wire_space + max_width
        y_pos = 0
        for r_svg, size in resistor_svgs:
            x_space = (max_width - size[
                0]) / 2  # space before r_svg (when r_svg is smaller than others, it is placed in middle)
            r_svg.translate(wire_space + x_space, y_pos)
            y_line = y_pos + size[1] / 2
            line_start = svgwrite.shapes.Line((half_wire_space, y_line), (wire_space + x_space, y_line),
                                              stroke=outline_color)
            x_line_end = wire_space + size[0] + x_space
            line_end = svgwrite.shapes.Line((x_line_end, y_line), (x_parallel_end, y_line), stroke=outline_color)
            y_pos += size[1] + resistor_space
            group.add(r_svg)
            group.add(line_start)
            group.add(line_end)
        height = y_pos - resistor_space  # the total height of all parallel resistor elements
        width = wire_space * 2 + max_width
        # small line on start
        y_start = resistor_svgs[0][1][1] / 2
        y_end = height - resistor_svgs[-1][1][1] / 2
        half_height = height / 2
        line_start = svgwrite.shapes.Line((0, half_height), (half_wire_space, half_height), stroke=outline_color)
        line_end = svgwrite.shapes.Line((width - half_wire_space, half_height), (width, half_height),
                                        stroke=outline_color)
        line_start_h = svgwrite.shapes.Line((half_wire_space, y_start), (half_wire_space, y_end), stroke=outline_color)
        line_end_h = svgwrite.shapes.Line((x_parallel_end, y_start), (x_parallel_end, y_end), stroke=outline_color)
        group.add(line_start)
        group.add(line_end)
        group.add(line_start_h)
        group.add(line_end_h)
        return group, (width, height)

    @property
    def resistors(self):
        return self._resistors


class SerialResistor(ParallelResistor):
    def __repr__(self):
        return "SerialResistor(" + ", ".join(repr(r) for r in self.resistors) + ")"
    
    def to_diagram(self):
        return "S(" + " + ".join(r.to_diagram() for r in self._resistors) + ")"
    
    def _recalc_resistance(self):
        return sum(r.resistance for r in self.resistors)
    
    def get_svg(self, resistor_size=(40, 10), wire_space=15, resistor_space=10, fill_color="rgb(218, 218, 218)",
                outline_color="black", text_color="black", font="Arial"):
        group = svgwrite.container.Group()
        if len(self.resistors) == 0:
            return group
        resistor_svgs = [r.get_svg(resistor_size, wire_space, resistor_space, fill_color, outline_color, text_color,
                                   font) for r in self._resistors]
        max_height = max(resistor_svgs, key=lambda x: x[1][1])[1][1]
        line_y = max_height / 2
        x_pos = wire_space
        line_start = svgwrite.shapes.Line((0, line_y), (x_pos, line_y), stroke="black")
        group.add(line_start)
        for r_svg, size in resistor_svgs:
            r_svg.translate(x_pos, (max_height - size[1]) / 2)
            x_pos += size[0]
            new_x_pos = x_pos + wire_space
            line = svgwrite.shapes.Line((x_pos, line_y), (new_x_pos, line_y), stroke="black")
            x_pos = new_x_pos
            group.add(r_svg)
            group.add(line)
        return group, (x_pos, max_height)


def parse_diagram(diagram):
    P = ParallelResistor
    S = SerialResistor
    R = Resistor
    return eval(diagram.replace("+", ",").replace("|", ","))
