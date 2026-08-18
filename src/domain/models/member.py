# src/domain/models/member.py

"""
Member Domain Model

Purpose
-------
Represents a unique OYBS member within the domain.

Responsibilities
----------------
- Store member identity.
- Validate member information.
- Provide normalized member data.
- Remain technology independent.

Notes
-----
- Immutable.
- Independent of attendance, activities and sessions.
- No UI, pandas or infrastructure dependencies.
"""

from __future__ import annotations

# Standard library imports
from dataclasses import dataclass
from typing import Final

# Third-party imports
# None

# Local imports
# None


@dataclass(frozen=True, slots=True)
class Member:
    """
    Immutable domain representation of a member.

    Attributes
    ----------
    name:
        Display name of the member.

    member_id:
        Optional unique identifier.

    phone_number:
        Optional phone number.

    unit:
        Optional church/unit/department.

    is_active:
        Indicates whether the member is active.
    """

    name: str
    member_id: str | None = None
    phone_number: str | None = None
    unit: str | None = None
    is_active: bool = True

    _MAX_NAME_LENGTH: Final[int] = 150

    def __post_init__(self) -> None:
        """Validate member information."""

        name = self.name.strip()

        if not name:
            raise ValueError("name cannot be empty.")

        if len(name) > self._MAX_NAME_LENGTH:
            raise ValueError(f"name cannot exceed {self._MAX_NAME_LENGTH} characters.")

        object.__setattr__(self, "name", name)

        if self.member_id is not None:
            member_id: str | None = self.member_id.strip()

            if not member_id:
                member_id = None

            object.__setattr__(self, "member_id", member_id)

        if self.phone_number is not None:
            phone: str | None = self.phone_number.strip()

            if not phone:
                phone = None

            object.__setattr__(self, "phone_number", phone)

        if self.unit is not None:
            unit: str | None = self.unit.strip()

            if not unit:
                unit = None

            object.__setattr__(self, "unit", unit)

    # ------------------------------------------------------------------
    # Derived Properties
    # ------------------------------------------------------------------

    @property
    def normalized_name(self) -> str:
        """
        Return a normalized version of the member name.

        Used for comparisons and lookups.
        """
        return " ".join(self.name.casefold().split())

    @property
    def display_name(self) -> str:
        """Return the preferred display name."""
        return self.name

    @property
    def initials(self) -> str:
        """Return member initials."""
        return "".join(word[0].upper() for word in self.name.split() if word)

    @property
    def has_phone_number(self) -> bool:
        """Return True if a phone number exists."""
        return self.phone_number is not None

    @property
    def has_member_id(self) -> bool:
        """Return True if a member ID exists."""
        return self.member_id is not None

    @property
    def has_unit(self) -> bool:
        """Return True if a unit exists."""
        return self.unit is not None

    # ------------------------------------------------------------------
    # Business Behaviour
    # ------------------------------------------------------------------

    def matches_name(self, name: str) -> bool:
        """
        Compare a supplied name against this member.

        Comparison is case-insensitive and ignores
        repeated whitespace.
        """
        normalized = " ".join(name.casefold().split())
        return normalized == self.normalized_name

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "name": self.name,
            "member_id": self.member_id,
            "phone_number": self.phone_number,
            "unit": self.unit,
            "is_active": self.is_active,
        }

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Return display representation."""
        return self.display_name

    def __repr__(self) -> str:
        """Return developer representation."""

        return f"Member(name={self.name!r}, member_id={self.member_id!r})"
