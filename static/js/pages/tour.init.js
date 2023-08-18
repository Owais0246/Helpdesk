$(document).ready(function () {
  hopscotch.startTour({
    id: "my-intro",
    steps: [
      {
        target: "ticket",
        title: "Raise a ticket",
        content: "To create a ticket, click the 'Raise a ticket' button ",
        placement: "bottom",
        yOffset: 10,
        xOffset: -105,
        arrowOffset: "center",
      },
      
    ],
    showPrevButton: !0,
  });
});
